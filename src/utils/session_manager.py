import uuid
from models.CommonModel import SessionDB, DB
import json
import traceback
__author__ = 'sam'


SESSION_SAVE_INTO_DB = 1


class Session(object):
    def __init__(self, session_id=None, expiry_time=0, save_location=SESSION_SAVE_INTO_DB):
        self.save_location = save_location
        self.session_id = session_id
        self.session_value = {}
        self.expiry_time = expiry_time

    def _get_session_from_db(self):
        rs = SessionDB.get(session_id=self.session_id)
        if rs:
            return rs
        else:
            raise Exception('Session %s No Found or Expiry' % self.session_id)

    def _set_session(self):
        sval_str = json.dumps(self.session_value)
        with DB.execution_context():
            if self.session_id:
                session = SessionDB.get(session_id=self.session_id)
                session.expiry_time = self.expiry_time
                session.sval = sval_str
                session.save()
            else:
                self.session_id = str(uuid.uuid4())
                SessionDB.create(session_id=self.session_id, sval=sval_str, expiry_time=self.expiry_time)

    def set_item(self, key, value):
        try:
            self._get_session()
            self.session_value.update({key: value})
            self._set_session()
        except Exception, e:
            raise Exception(
                'an error happens in set_item of Session, error:%s, detail:%s' % (str(e), traceback.format_exc()))

    def get_item(self, key, default_value=None):
        try:
            self._get_session()
            return self.session_value.get(key, default_value)
        except Exception, e:
            raise Exception(
                'an error happens in get_item of Session, error:%s, detail:%s' % (str(e), traceback.format_exc()))

    def _get_session(self):
        if self.save_location == SESSION_SAVE_INTO_DB:
            if self.session_id and self.session_value == {}:
                result = self._get_session_from_db()
                self.session_value = json.loads(result.sval) if result.sval else {}
                self.expiry_time = result.expiry_time
        else:
            raise Exception('incorrect session save location')
