from pg_common import SingletonBase, log_error, log_info
from pg_environment import config
from pg_redis import RedisManager
import json


__all__ = ("GameConfigManager", "GamePropertyManager")


GAME_CONFIG_REDIS_KEY = "__GAME_CONFIG__"
GAME_PROPERTY_REDIS_KEY = "__GAME_PROPERTY__"


class _GamePropertyManager(SingletonBase):
    def __init__(self):
        self._cfg: dict[str, dict] = {}

    async def reload(self):
        _r = await RedisManager.get_redis()
        if _r:
            _prop = await _r.get(GAME_PROPERTY_REDIS_KEY)
            if _prop:
                self._cfg = json.loads(_prop)
                log_info("load game property success.")
            else:
                log_error(f"!!!can not get key {GAME_PROPERTY_REDIS_KEY} in redis.")
        else:
            log_error("!!!!can not get redis client.")

    def get_config(self):
        if self._cfg:
            return self._cfg
        else:
            return config.get_conf("game_property", {})

class _GameConfigManager(SingletonBase):
    def __init__(self):
        self._cfg: dict[str, dict] = {}

    async def reload(self):
        _r = await RedisManager.get_redis()
        if _r:
            _games = await _r.smembers(GAME_CONFIG_REDIS_KEY)
            for _g in _games:
                _json = await _r.get("%s:%s" % (GAME_CONFIG_REDIS_KEY, _g))
                if _json:
                    self._cfg[_g] = json.loads(_json)
                    log_info(f"===[{_g}]:[{self._cfg[_g]['version']}]===")

        else:
            log_error("!!!!!!!can not get redis client.")

    def get_config(self, game: str) -> dict:
        if game in self._cfg:
            return self._cfg[game]
        return None


GameConfigManager = _GameConfigManager()
GamePropertyManager = _GamePropertyManager()
