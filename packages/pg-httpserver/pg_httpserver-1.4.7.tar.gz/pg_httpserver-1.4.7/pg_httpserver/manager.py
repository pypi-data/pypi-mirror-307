from pg_common import SingletonBase, log_error, log_info
from pg_environment import config
from pg_redis import RedisManager
from .define import ExCodeCfg
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


class _GameExCodeManager(SingletonBase):
    def __init__(self):
        self._ex_cfg:dict[str, dict[int, ExCodeCfg]] = {}
        self._manual_code:[str, dict[str, ExCodeCfg]]= {}

    def reload(self, data:[], game: str):
        for d in data:
            _c = ExCodeCfg(**d)
            if game not in self._ex_cfg:
                self._ex_cfg[game] = {}
            _manual_key = "_".join([game, _c.channel])
            if _manual_key not in self._manual_code:
                self._manual_code[_manual_key] = {}
            self._ex_cfg[game][d['id']] = _c
            if not _c.auto_gen:
                _codes = _c.code.split(",")
                for _code in _codes:
                    if _code:
                        self._manual_code[_manual_key][_code] = _c

    def get_by_id(self, game, _id)->ExCodeCfg:
        if game in self._ex_cfg and _id in self._ex_cfg[game]:
            return self._ex_cfg[game][_id]
        return None

    def get_by_code(self, game, channel, code)->ExCodeCfg:
        key = "_".join([game, channel])
        if key in self._manual_code and code in self._manual_code[key]:
            return self._manual_code["_".join([game, channel])][code]
        return None


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

                    if "excodes" in self._cfg[_g]:
                        GameExCodeManager.reload(self._cfg[_g]['excodes'], _g)
                    else:
                        log_info(f"---[{_g}]:has no ex code config---")

        else:
            log_error("!!!!!!!can not get redis client.")

    def get_config(self, game: str) -> dict:
        if game in self._cfg:
            return self._cfg[game]
        return None


GameConfigManager = _GameConfigManager()
GamePropertyManager = _GamePropertyManager()
GameExCodeManager = _GameExCodeManager()
