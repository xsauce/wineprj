import settings
import json

__author__ = 'samgu'


class Cache(object):
    def __init__(self):
        self._data = {}
        self._ddata = {}
        cache_conf = settings.CACHE_CONF
        if cache_conf['type'] == 'json_file':
            self.cache_uri = cache_conf['uri']

    def _get_from_jsonfile(self):
        d = {}
        with open(self.cache_uri, 'r') as f:
            txt = f.read()
            self._data = json.loads(txt)

    def get(self, key):
        if not self._data:
            self._get_from_jsonfile()
        return self._data.get(key)


cache = Cache()
