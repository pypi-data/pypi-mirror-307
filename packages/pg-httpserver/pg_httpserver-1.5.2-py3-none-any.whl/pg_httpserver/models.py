from pg_ormapping import ObjectBase, ObjectType, GlobalRedisKey, IntField, StringField
from enum import unique
from .define import SESSION_EXPIRED_TIME


@unique
class RedisKey(GlobalRedisKey):
    ReqData = "req_data"


class ReqData(ObjectBase):
    __redis_key__ = RedisKey.ReqData
    __obj_type__ = ObjectType.REDIS
    __redis_expire_in__ = SESSION_EXPIRED_TIME
    uid = IntField("uid", primary_key=True)
    req_cnt = IntField("req_cnt")
    last_resp = StringField('last_resp')
    last_header = StringField('last_head')

