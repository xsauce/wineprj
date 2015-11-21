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
_sqlite3_db_conf = {
        'uri': os.path.join(ROOT_DIR, 'test.db')
    }
_mongo_db_conf = {
    'uri': 'mongodb://winedb:' + urllib.quote_plus('winedb$123') + '@52.192.129.192:27017'
}
_mongo_test_conf = {
    'uri': 'mongodb://localhost:27017'
}

DB_CONFIG = {
    'wineshop': {
        'type': 'mongodb',
        'conf': _mongo_test_conf
    }
}
# ---
PHOTO_DIR = os.path.join(ROOT_DIR, 'static', 'photo')
CURRENT_DB = 'wineshop'
LOG_CONF = {
    'dir': '/var/log/wineprj',
    'level': 'DEBUG'
}

COOKIE_EXPIRY_DAYS = 0.5

DEBUG = True



APP_SETTINGS = {
    'autoreload': DEBUG,
    'static_hash_cache': (not DEBUG),
    'serve_traceback': DEBUG,
    'debug': DEBUG,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'compiled_template_cache': (not DEBUG),
    'cookie_secret': str(uuid.uuid4())
}


