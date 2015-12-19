import uuid
from utils.sqlhelper import SqlHelper, WHERE_CONDITION

__author__ = 'sam'
import json
import traceback

SESSION_SAVE_INTO_DB = 1

class Session(object):
    def __init__(self, session_id=None, expiry_days=0, save_location=SESSION_SAVE_INTO_DB):
        self.save_location = save_location
        self.session_id = session_id
        self.session_value = {}
        self.expiry_days = expiry_days

    def _query_session_by_id(self, session_id):
        sqlhelper = SqlHelper()
        where_value, where_str = WHERE_CONDITION.EXACT('sid', session_id)
        rs = sqlhelper.query_one('select sid, sval, expiry_time from session where %s' % where_str, where_value)
        if rs:
            return rs
        else:
            raise Exception('Session %s No Found or Expiry' % session_id)

    def _set_session(self, value_str, expiry_time, session_id=''):
        session_id = session_id if session_id else str(uuid.uuid4())
        sqlhelper = SqlHelper()
        sqlhelper.execute('''
            insert into session(sid, sval, expiry_time, created_at, updated_at)
            values(%s, %s, %s, NOW(), NOW())
            ON DUPLICATE KEY UPDATE sval=values(sval), expiry_time=values(expiry_time);''', (session_id, value_str, expiry_time))
        sqlhelper.commit()
        sqlhelper.close()
        return session_id

    def set_item(self, key, value):
        try:
            if self.save_location == SESSION_SAVE_INTO_DB:
                self._get_session()
                self.session_value.update({key: value})
                value_str = json.dumps(self.session_value)
                if not self.session_id:
                    self.session_id = self._set_session(value_str=value_str, expiry_time=self.expiry_days)
                else:
                    self._set_session(value_str=value_str, expiry_time=self.expiry_days, session_id=self.session_id)
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
                result = self._query_session_by_id(self.session_id)
                value = result.get('sval', None)
                self.session_value = json.loads(value) if value else {}
                self.expiry_days = result['expiry_time']
            else:
                raise Exception('incorrect session save location')
        else:
            self.session_value = {}

