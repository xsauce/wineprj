from bson import ObjectId

__author__ = 'sam'
import json
import traceback
from utils.mongohelper import MongoHelper
from settings import COOKIE_EXPIRY_DAYS

SESSION_SAVE_INTO_DB = 1

class Session(object):
    def __init__(self, session_id=None, expiry_days=COOKIE_EXPIRY_DAYS, save_location=SESSION_SAVE_INTO_DB):
        self.save_location = save_location
        self.session_id = session_id
        self.session_value = {}
        self.expiry_days = expiry_days

    def set_item(self, key, value):
        try:
            if self.save_location == SESSION_SAVE_INTO_DB:
                db = MongoHelper().connect()
                self._get_session()
                self.session_value.update({key: value})
                value_str = json.dumps(self.session_value)
                if not self.session_id:
                    result = db.session.insert_one({'value': value_str, 'expiry_time': self.expiry_days})
                    self.session_id = str(result.inserted_id)
                else:
                    result = db.session.update_one({'_id': ObjectId(self.session_id)}, {'value': value_str, 'expiry_time': self.expiry_days})
                    if result.modified_count != 1 and result.matched_count != 1:
                        raise Exception('fail to update session, modified_count:%s, matched_count:%s', (result.modified_count, result.matched_count))
            else:
                raise Exception('incorrect session save location')
        except Exception, e:
            raise Exception('an error happens in set_item of Session, error:%s, detail:%s' % (str(e), traceback.format_exc()))

    def get_item(self, key, default_value=None):
        try:
            if not self.session_value:
                self._get_session()
            return self.session_value.get(key, default_value)
        except Exception, e:
            raise Exception('an error happens in get_item of Session, error:%s, detail:%s' % (str(e), traceback.format_exc()))

    def _get_session(self):
        if self.session_id:
            if self.save_location == SESSION_SAVE_INTO_DB:
                db = MongoHelper().connect()
                result = db.session.find_one({'_id': ObjectId(self.session_id)})
                value = result.get('value', None)
                self.session_value = json.loads(value) if value else {}
                self.expiry_days = result['expiry_days']
            else:
                raise Exception('incorrect session save location')
        else:
            self.session_value = {}
            self.expiry_days = COOKIE_EXPIRY_DAYS

