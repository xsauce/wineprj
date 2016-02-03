import os
import urllib
import uuid

__author__ = 'gx'


ROOT_DIR = os.path.dirname(__file__)

#register models file
MODEL_MODULES = (
    'models.wineshop',
)

# DB settings
_mongo_db_conf = {
    'uri': 'mongodb://winedb:' + urllib.quote_plus('winedb$123') + '@52.192.129.192:27017'
}
_mysql_db_conf = {
    'host': 'localhost',
    'port': 3306,
    'user': 'wineprj',
    'password': 'wineprj$123'
}

DB_CONFIG = {
    'wineprj': {
        'type': 'mysql',
        'conf': _mysql_db_conf
    }
}
# ---
PHOTO_DIR = os.path.join(ROOT_DIR, 'static', 'photo')
CURRENT_DB = 'wineprj'
LOG_CONF = {
    'dir': '/var/log/wineprj',
    'level': 'DEBUG'
}

LOCALE_DIR = os.path.join(ROOT_DIR, 'locale')

SESSION_EXPIRY_MINUTES = 24 * 60

DEBUG = True

CACHE_CONF = {
    'type': 'json_file',
    'uri': os.path.join(ROOT_DIR, 'cache.json')
}

APP_SETTINGS = {
    'autoreload': DEBUG,
    'static_hash_cache': (not DEBUG),
    'serve_traceback': DEBUG,
    'debug': DEBUG,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'compiled_template_cache': (not DEBUG),
    'cookie_secret': 'wineprj' if DEBUG else str(uuid.uuid4())
}
