# -*-coding:utf8;-*-
from zcache.Storage.BaseFileStorage import BaseFileStorage
import time


class Database:
    """
    main zcache Core.
    """

    def __init__(self, path=None, limit=0, storage=None, plugins=None):
        self.plugins = plugins
        if path is not None:
            path = path
        else:
            path = "zcache.json"
        if storage is not None:
            self.storage = storage
        else:
            self.storage = BaseFileStorage(path)
        self.__limit = limit
        self.__loadfile()

    def __updatefile(self):
        self.storage.save(self.databases)

    def __loadfile(self):
        self.databases = self.storage.load()
        self.databases["limit"] = self.__limit

    def __exists(self, key):
        try:
            t = self.databases["data"][key]
            if t["ttl"] != 0:
                sisa = int(time.time()) - t["time"]
                if sisa >= t["ttl"]:
                    if self.plugins is not None:
                        self.plugins.on_expired(self, key)
                    del self.databases["data"][key]
                    self.__updatefile()
                    return False, False
                else:
                    return True, t["content"]
            else:
                return True, t["content"]
        except KeyError:
            return False, False

    def __set(self, key, value, ttl=0):
        if self.plugins is not None:
            value = self.plugins.on_write(self, key, value)
        data = {}
        data["time"] = int(time.time())
        data["ttl"] = ttl
        data["content"] = value
        self.databases["data"][key] = data
        self.__updatefile()

    def has(self, key):
        if not isinstance(key, str):
            raise TypeError
        self.__loadfile()
        r, v = self.__exists(key)
        return r

    def get(self, key, default=None):
        if not isinstance(key, str):
            raise TypeError
        self.__loadfile()
        r, v = self.__exists(key)
        if r:
            if self.plugins is not None:
                return self.plugins.on_read(self, key, v)
            return v
        else:
            return default

    def set(self, key, value, ttl=0):
        if not isinstance(key, str):
            raise TypeError
        # to optimize, __loadfile() not called here because already called in size()
        size = self.size()
        if self.databases["limit"] != 0:
            if self.databases["limit"] == size:
                if self.plugins is not None:
                    self.plugins.on_limit(self, key, value, ttl)
                return False
            else:
                self.__set(key, value, ttl)
                return True
        else:
            self.__set(key, value, ttl)
            return True

    def delete(self, key):
        if not isinstance(key, str):
            raise TypeError
        # to optimize, __loadfile() not called here because already called in has()
        check = self.has(key)
        if check:
            if self.plugins is not None:
                self.plugins.on_delete(self, key)
            del self.databases["data"][key]
            self.__updatefile()
            return True
        else:
            return False

    def size(self):
        self.__loadfile()
        ret = len(self.databases["data"])
        return ret

    def reset(self):
        self.__loadfile()
        self.databases["data"] = {}
        self.__updatefile()
