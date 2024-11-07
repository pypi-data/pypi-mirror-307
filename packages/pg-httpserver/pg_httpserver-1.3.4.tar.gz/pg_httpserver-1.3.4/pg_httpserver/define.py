from pg_resourceloader import LoaderManager
from pg_common import FuncDecoratorManager
from pg_environment import config
from typing import Dict, Union, Tuple, Optional
from pg_common import datetime_now, datetime_2_timestamp, DictValType
from pydantic import BaseModel
from enum import Enum, unique


__all__ = [
    "ENV_HANDLER_DIR", "httpserver_init", "ENV_NEEDS_BODY_MIDDLEWARE", "ENV_CHECK_SESSION_HEADER_KEY",
    "ENV_NEEDS_GAME_CONFIG", "ENV_NEEDS_GAME_PROPERTY", "ENV_NEEDS_CHECK_SESSION", "ENV_CHECK_SESSION_IGNORE_URI",
    "GameException", "GameErrorCode", "FieldContainer", "ResponseMap", "ResponseHeader", "ResponseData", "RequestMap",
    "RequestHeader", "RequestData", "Context", "SESSION_EXPIRED_TIME", "ENV_CONTEXT_KEY", "SessionUser", "BaseInfo",
    "GenderType", "PlatType", "LangType"
]
__auth__ = "baozilaji@gmail.com"


ENV_HANDLER_DIR = "handler_dir"
ENV_NEEDS_BODY_MIDDLEWARE = "needs_body_middleware"
ENV_NEEDS_GAME_CONFIG = "needs_game_config"
ENV_NEEDS_GAME_PROPERTY = "needs_game_property"
ENV_NEEDS_CHECK_SESSION = "needs_check_session"
ENV_CHECK_SESSION_IGNORE_URI = "check_session_ignore_uri"
ENV_CHECK_SESSION_HEADER_KEY = "check_session_header_key"
ENV_CONTEXT_KEY = "context_key"
"""
http server configuration
{
  "handler_dir": "handler",
  "needs_body_middleware": true,
  "needs_game_config": false,
  "needs_game_property": false,
  "needs_check_session": false,
  "check_session_ignore_uri": ['/test_uri',],
  "check_session_header_key": "Authentication",
  "context_key": "_context_",
}
"""


def httpserver_init():
    FuncDecoratorManager.scan_decorators(config.get_conf(ENV_HANDLER_DIR, "handlers"))
    LoaderManager.scan_loaders()


SESSION_EXPIRED_TIME = 3600


class GameErrorCode(object):
    RECEIVE_INPUT_ERROR = -100000
    NO_MATCHED_METHOD_ERROR = -100001
    OTHER_EXCEPTION = -100002


class GameException(Exception):

    def __init__(self, state: int, msg: str):
        self.state = state
        self.msg = msg

    def __str__(self):
        return f"\"{self.state}, {self.msg}\""

    def __repr__(self):
        return self.__str__()


@unique
class LangType(Enum):
    zh_CN = "zh-CN"
    en_US = "en-US"


@unique
class PlatType(Enum):
    ios = "ios"
    android = "and"
    html5 = "h5"
    windows = "win"

@unique
class GenderType(Enum):
    male = "male"
    female = "female"
    unknown = "unknown"


"""
BaseInfo对象，如果数据结构变化，依赖的模块都需要更新重启
"""
class BaseInfo(BaseModel):
    uid: int
    open_id: str
    name: Optional[str] = ''
    head_url: Optional[str] = ''
    gender: Optional[int] = 0

class SessionUser(BaseModel):
    uid: int
    open_id: str
    sessionKey: str
    last_req: int
    game: str
    channel: str
    version: int
    plat: PlatType
    lang: LangType
    info: Optional[BaseInfo] = None
    gm: Optional[str] = None


class FieldContainer(object):
    def __init__(self):
        self._content: dict[str, set[str]] = {}

    def add(self, obj:str, field: str):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].add(field)

    def add_many(self, obj: str, fields: Union[set[str], list[str], Tuple[str]]):
        if obj not in self._content:
            self._content[obj] = set()
        self._content[obj].update(fields)

    def __str__(self):
        return str(self._content)


class ResponseMap(BaseModel):
    method: str = ""
    retCode: int = 0


class ResponseHeader(BaseModel):
    datas: list[ResponseMap] = []
    retCode: int = 0 # 错误码
    st: int = 0 # 自增计数
    token: str = "" # 单点登陆的token
    ts: int = int(datetime_2_timestamp(datetime_now())) # 时间（秒）
    offSt: int = 0 # 离线请求自增计数
    msg: str = "" # 消息


class ResponseData(BaseModel):
    head: ResponseHeader
    body: dict


class RequestMap(BaseModel):
    method: str = ""
    data: str = ""
    param: dict = {}


class RequestHeader(BaseModel):
    datas: list[RequestMap] = []
    mv: int = 0 # meta版本号
    uuid: str = "" # session key
    st: int = 0 # 自增计数
    token: str = "" # 单点登陆的token
    offSt: int = 0 # 离线请求自增计数
    rv: int = 0 # res版本号
    extra: str = "" # 额外数据，如network环境等
    pj: str = "" # 项目名称


class RequestData(BaseModel):
    head: RequestHeader
    body: dict


class Context(BaseModel):
    log: dict[str, DictValType] = {}
    req: Optional[dict] = {}
    resp: Optional[dict] = {}
    path: Optional[str] = ''
    user: Optional[SessionUser] = None