import datetime

from pg_resourceloader import LoaderManager
from pg_common import FuncDecoratorManager, Context, PlatType, RewardItem
from pg_environment import config
from pg_ormapping import ObjectBase
from typing import Union, Tuple, Optional
from pg_common import datetime_now, datetime_2_timestamp
from pydantic import BaseModel


__all__ = [
    "ENV_HANDLER_DIR", "httpserver_init", "ENV_NEEDS_BODY_MIDDLEWARE", "ENV_CHECK_SESSION_HEADER_KEY",
    "ENV_NEEDS_GAME_CONFIG", "ENV_NEEDS_GAME_PROPERTY", "ENV_NEEDS_CHECK_SESSION", "ENV_CHECK_SESSION_IGNORE_URI",
    "GameException", "GameErrorCode", "FieldContainer", "ResponseMap", "ResponseHeader", "ResponseData", "RequestMap",
    "RequestHeader", "RequestData", "SESSION_EXPIRED_TIME", "ENV_CONTEXT_KEY", "GameContext", "ExCodeCfg",
    "ENV_NEEDS_CHECK_REQUEST_ID", "ENV_CHECK_REQUEST_ID_IGNORE_URI", "ENV_GAME_CONTEXT_KEY"
]
__auth__ = "baozilaji@gmail.com"


ENV_HANDLER_DIR = "handler_dir"
ENV_NEEDS_BODY_MIDDLEWARE = "needs_body_middleware"
ENV_NEEDS_GAME_CONFIG = "needs_game_config"
ENV_NEEDS_GAME_PROPERTY = "needs_game_property"
ENV_NEEDS_CHECK_SESSION = "needs_check_session"
ENV_CHECK_SESSION_IGNORE_URI = "check_session_ignore_uri"
ENV_NEEDS_CHECK_REQUEST_ID = "needs_check_request_id"
ENV_CHECK_REQUEST_ID_IGNORE_URI = "check_request_id_ignore_uri"
ENV_CHECK_SESSION_HEADER_KEY = "check_session_header_key"
ENV_CONTEXT_KEY = "context_key"
ENV_GAME_CONTEXT_KEY = "game_context_key"
"""
http server configuration
{
  "handler_dir": "handler",
  "needs_body_middleware": true,
  "needs_game_config": false,
  "needs_game_property": false,
  "needs_check_session": false,
  "check_session_ignore_uri": ["/test_uri"],
  "needs_check_request_id": true,
  "check_request_id_ignore_uri": ["/game_info"],
  "check_session_header_key": "Authentication",
  "context_key": "_context_",
  "game_context_key": "_game_context_",
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


class ExCodeCfg(BaseModel):
    id: int
    channel: str
    plat: list[PlatType]
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    code: str
    rewards: list[RewardItem]
    auto_gen: bool



"""
请求协议函数中使用，用于缓存一次请求过程中，所有从db层读取到的数据
处理所有加载数据中的细节，比如redis的prefix，redis的实例配置，mongo的实例配置，数据库信息等
redis数据配置用根对象下的redis对象中的`game`_`channel`对象
redis的prefix也使用`game`_`channel`拼接字符串
{
    "redis":{
        "duck_qa": {
            
        }
    }
}
mongo同理
{
    "mongodb": {
        "duck_qa": {
            
        }
    }
}
"""
class GameContext(object):
    def __init__(self, ctx: Context):
        self.ctx = ctx
        self.cache = {}

    def _get_key(self):
        return "_".join([self.ctx.user.game, self.ctx.user.channel])

    def get_db_source(self):
        return self._get_key()

    def get_db_name(self):
        return self._get_key()

    def get_redis_server_name(self):
        return self._get_key()

    def get_redis_prefix(self):
        return self._get_key()

    async def load_data(self, clazz, pri_keys: dict)->ObjectBase:
        name = clazz.__name__
        key = self._get_key()
        if name not in self.cache:
            ret = clazz()
            self.cache[name] = ret
            for k, v in pri_keys.items():
                ret[k] = v

            await ret.load(prefix=key, redis_server_name=key,
                           db_name=key, db_source=key)
        else:
            ret = self.cache[name]
        ret.init_after_load(prefix=key, redis_server_name=key,
                           db_name=key, db_source=key)
        return ret