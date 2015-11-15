import settings
from utils.logger import get_logger
__author__ = 'sam'
from pymongo import MongoClient


class MongoHelper(object):

    def __init__(self, db_name=settings.CURRENT_DB):
        self.db_name = db_name
        self.db_conf = settings.DB_CONFIG[self.db_name]['conf']
        self.logger = get_logger('mongo_helper')

    def connect(self):
        try:
            self.client = MongoClient(
                self.db_conf['host'],
                self.db_conf['port'])
            return self.client[self.db_name]
        except Exception, e:
            self.logger.critical(str(e))

    def close(self):
        try:
            self.client.close()
        except Exception, e:
            self.logger.critical(str(e))

    def __del__(self):
        self.close()


