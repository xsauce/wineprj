import os
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
    'host': 'localhost',
    'port': 27017
}

DB_CONFIG = {
    'wineshop': {
        'type': 'mongodb',
        'conf': _mongo_db_conf
    }
}
# ---
PHOTO_DIR = os.path.join(ROOT_DIR, 'static', 'photo')
CURRENT_DB = 'wineshop'
LOG_CONF = {
    'dir': os.path.join(ROOT_DIR, 'log'),
    'level': 'DEBUG'
}

DEBUG = True

APP_SETTINGS = {
    'autoreload': DEBUG,
    'static_hash_cache': (not DEBUG),
    'serve_traceback': DEBUG,
    'debug': DEBUG,
    'static_path': os.path.join(ROOT_DIR, 'static'),
    'template_path': os.path.join(ROOT_DIR, 'templates'),
    'compiled_template_cache': (not DEBUG),
}


