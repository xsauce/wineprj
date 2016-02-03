# coding: utf-8
from functools import partial
import json
import urllib
from tornado.web import RequestHandler
import settings
from utils.logger import get_logger
from utils.session_manager import Session

COOKIE_SESSION_NAME = 'session_id'


class CommonHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(CommonHandler, self).__init__(*args, **kwargs)
        self.logger = get_logger('wineshop')
        self._session = None

    def get_current_user(self):
        return self.get_session().get_item('user')

    def get_session(self):
        session_id = self.get_secure_cookie(COOKIE_SESSION_NAME)
        if self._session is None:
            self._session = Session(session_id=session_id, expiry_time=settings.SESSION_EXPIRY_MINUTES)
        return self._session

    def set_session_item(self, key, value):
        self.logger.debug('set session key %s value %s' % (key, value))
        self.get_session().set_item(key, value)
        self.set_secure_cookie(COOKIE_SESSION_NAME, self._session.session_id, expires_days=self._session.expiry_time / 60 * 24)


class WineShopCommonHandler(CommonHandler):
    def __init__(self, *args, **kwargs):
        super(WineShopCommonHandler, self).__init__(*args, **kwargs)
        self._ul = self.get_browser_locale().translate

    def _get_errmsg(self, status_code):
        if status_code == '404':
            return self._ul('page_not_found')
        elif status_code == '500':
            return self._ul('try_again')

    def _get_shopcar_cookie(self):
        shopcar = self.get_cookie('shopcar', None)
        if shopcar:
            shopcar = urllib.unquote(shopcar)
            return shopcar.split(',')
        else:
            return []

    def write_error(self, status_code, **kwargs):
        self.logger.error('status_code:%s, errmsg:%s' % (status_code, kwargs))
        if settings.DEBUG:
            errmsg = 'status_code:' + str(status_code) + ',' + unicode(kwargs)
        else:
            errmsg = self._get_errmsg(status_code)
        self.page_render('wineshop/tip.html', tip=errmsg)

    def page_render(self, template, **kwargs):
        shopcar = self._get_shopcar_cookie()
        kwargs.update({'count_in_shopcar': len(shopcar)})
        user_str = self.get_current_user()
        if user_str:
            user = json.loads(user_str)
        else:
            user = {}
        kwargs.update({'username': user.get('username', '')})
        kwargs.update({'_ul': self._ul})
        self.render(template, **kwargs)
