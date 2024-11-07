import json
import time

from fastapi import FastAPI, applications, status
from contextlib import asynccontextmanager
import asyncio
from pg_objectserialization import loads, dumps
import uvicorn
from starlette.datastructures import MutableHeaders
from pg_common import log_info, log_error, start_coroutines, base64_decode, base64_encode, \
    GLOBAL_DEBUG, fernet_decrypt, fernet_encrypt
from pg_environment import config
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from .define import ENV_NEEDS_BODY_MIDDLEWARE, ENV_NEEDS_CHECK_SESSION, ENV_CHECK_SESSION_IGNORE_URI, \
    ENV_NEEDS_GAME_CONFIG, ENV_NEEDS_GAME_PROPERTY, ENV_CHECK_SESSION_HEADER_KEY, GameException, GameErrorCode, \
    SESSION_EXPIRED_TIME, Context, ENV_CONTEXT_KEY, SessionUser
from .manager import GameConfigManager, GamePropertyManager
CODE_VERSION = 0

__all__ = [
           "run", "app", "CODE_VERSION", "get_session_user", "get_context"
           ]
__auth__ = "baozilaji@gmail.com"


def swagger_ui_html_patch(*args, **kwargs):
    return get_swagger_ui_html(*args, **kwargs,
                               swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
                               swagger_css_url="/static/swagger-ui/swagger-ui.css")

applications.get_swagger_ui_html = swagger_ui_html_patch

@asynccontextmanager
async def life_span(_app: FastAPI):
    from pg_httpserver import httpserver_init
    httpserver_init()
    start_coroutines(reload_config())
    log_info("http server startup")
    yield
    global _RUNNING
    _RUNNING = False
    log_info("http server shutdown")


app = FastAPI(docs_url=None if config.is_prod() else "/docs", lifespan=life_span)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

_RUNNING = True


def reload_code_version():
    global CODE_VERSION
    if not CODE_VERSION:
        with open("VERSION") as _f:
            CODE_VERSION = int(_f.read())
            log_info(f"code version is: {CODE_VERSION}")


async def reload_config():
    while _RUNNING:
        try:
            reload_code_version()
            if config.get_conf(ENV_NEEDS_GAME_CONFIG, False):
                await GameConfigManager.reload()
            if config.get_conf(ENV_NEEDS_GAME_PROPERTY, False):
                await GamePropertyManager.reload()
        except Exception as e:
            log_error(e)
        await asyncio.sleep(60)
    log_info(f"server stopped")


@app.get("/health", description="健康检查接口", response_description="返回代码版本号")
async def health():
    return {
        "status": 0,
        "info": "OK",
        "code_version": CODE_VERSION
    }

class _CustomBodyResponder:
    def __init__(self, _app):
        self.app = _app
        self.initial_message = {}

    async def __call__(self, scope, receive, send) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send
        await self.app(scope, self.receive_with_msg, self.send_with_msg)

    async def receive_with_msg(self):
        message = await self.receive()
        _body: bytes = message.get("body", b"")
        if _body:
            _body = base64_decode(_body)
            _body = loads(_body, p=GLOBAL_DEBUG)
            _container_key = config.get_conf(ENV_CONTEXT_KEY, "_context_")
            self.scope[_container_key].log['req'] = _body
            _body = json.dumps(_body)
            _body = _body.encode()
            message["body"] = _body
        return message
    async def send_with_msg(self, message):
        if message["type"] == "http.response.start":
            self.initial_message = message
            return

        elif message["type"] == "http.response.body":
            headers = MutableHeaders(raw=self.initial_message['headers'])
            body = message['body']
            body = body.decode()
            body = json.loads(body)
            _container_key = config.get_conf(ENV_CONTEXT_KEY, "_context_")
            self.scope[_container_key].log['resp'] = body
            body = base64_encode(dumps(body, p=GLOBAL_DEBUG))
            message["body"] = body
            headers["Content-Type"] = "text/plain"
            headers["Content-Length"] = str(len(body))
            self.initial_message['headers'] = headers.items()
            await self.send(self.initial_message)
            await self.send(message)

class CustomBodyMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http" or scope["method"] != "POST":
            await self.app(scope, receive, send)
            return

        responder = _CustomBodyResponder(self.app)
        await responder(scope, receive, send)

if config.get_conf(ENV_NEEDS_BODY_MIDDLEWARE, default=True):
    log_info(f"add custom middleware to encrypt response and decrypt request")
    app.add_middleware(CustomBodyMiddleware)


if config.get_conf(ENV_NEEDS_CHECK_SESSION, default=True):
    log_info(f"add custom middleware to check session")
    @app.middleware("http")
    async def http_inspector(request, call_next):
        if request.method != "POST":
            return await call_next(request)

        _uri = request.scope['path']
        _ignores = config.get_conf(ENV_CHECK_SESSION_IGNORE_URI, [])
        _ignore = any([_uri.rfind(_i)>=0 for _i in _ignores])

        if _ignore:
            return await call_next(request)
        _header_key = config.get_conf(ENV_CHECK_SESSION_HEADER_KEY, default="Authentication")
        if _header_key not in request.headers:
            return PlainTextResponse("FORBIDDEN1", status_code=status.HTTP_403_FORBIDDEN)

        _header = request.headers[_header_key]
        _payload = _header.split(" ")
        if len(_payload) != 2:
            return PlainTextResponse("FORBIDDEN2", status_code=status.HTTP_403_FORBIDDEN)
        _game, _token = _payload
        _cfg = GamePropertyManager.get_config()
        if _game not in _cfg:
            return PlainTextResponse("FORBIDDEN3", status_code=status.HTTP_403_FORBIDDEN)

        _fernet_key = _cfg[_game]['fernet_key'].encode()
        # _user = json.loads(rsa_decrypt2(_token, _cfg[_game]['pri_key']))
        _user = json.loads(fernet_decrypt(_token.encode(), _fernet_key))
        _session_user = SessionUser(**_user)
        _ctx = get_context(request)
        _ctx.log.update({'uid': _session_user.uid, 'open_id': _session_user.open_id, 'version': _session_user.version,
                         'gm': _session_user.gm})

        _now = int(time.time())
        if _now - _session_user.last_req >= SESSION_EXPIRED_TIME:
            return PlainTextResponse("UNAUTHORIZED1", status_code=status.HTTP_401_UNAUTHORIZED)

        # 调用gm接口，却没有gm权限
        if _uri.rfind("/gm/") >=0 and not _session_user.gm:
            return PlainTextResponse("UNAUTHORIZED2", status_code=status.HTTP_401_UNAUTHORIZED)

        _session_user.last_req = _now

        _ctx.user = _session_user
        response = await call_next(request)

        # 如果存在session中还存在info对象，直接删除（这里隐性约定convert接口之后的第二个协议就应该将info的属性转存起来）
        if 'info' in _user:
            del _user['info']

        # response.headers[_header_key] = " ".join([_game, rsa_encrypt2(json.dumps(_user), _cfg[_game]['pub_key'])])
        response.headers[_header_key] = " ".join([_game, fernet_encrypt(_session_user.json().encode(), _fernet_key).decode()])
        return response


def get_context(req: Request)->Context:
    return req.scope[config.get_conf(ENV_CONTEXT_KEY, "_context_")]


def get_session_user(req: Request)->SessionUser:
    return get_context(req).user


@app.middleware("http")
async def http_log_inspector(request, call_next):
    if request.method != 'POST':
        return await call_next(request)

    _start_time = time.perf_counter()
    _container = Context(path=request.scope['path'])
    request.scope[config.get_conf(ENV_CONTEXT_KEY, "_context_")] = _container
    response = await call_next(request)
    _process_time = time.perf_counter() - _start_time
    _container.log.update({"process_time": _process_time, "path": _container.path})
    log_info(_container.log)
    return response


def run(port=None, reload=False):
    uvicorn.run(app="pg_httpserver.fapi:app", host=config.get_host(), reload=reload,
                port=config.get_port() if port is None else port)