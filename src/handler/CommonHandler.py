# coding: utf-8
import json
import urllib
from tornado.web import RequestHandler
import settings
from utils.logger import get_logger
from utils.session_manager import Session

COOKIE_SESSION_NAME = 'session_id'

class CommonHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        self.logger = get_logger('wineshop')
        self._session = None
        super(CommonHandler, self).__init__(*args, **kwargs)

    def get_current_user(self):
        return self.session.get_item('user')

    @property
    def session(self):
        session_id = self.get_secure_cookie(COOKIE_SESSION_NAME)
        if self._session is None:
            self._session = Session(session_id=session_id)
        return self._session

    def create_session_and_set_item(self, key, value, expiry_days=settings.SESSION_EXPIRY_DAYS):
        self.logger.debug('set session key %s value %s' % (key, value))
        self._session = Session(expiry_days=expiry_days)
        self.session.set_item(key, value)
        self.set_secure_cookie(COOKIE_SESSION_NAME, self._session.session_id, expires_days=expiry_days)


class WineShopCommonHandler(CommonHandler):
    def _get_errmsg(status_code):
        if status_code == '404':
            return u'您访问的页面没有找到'
        elif status_code == '500':
            return u'系统正忙，稍后重试'
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
        user_str = self.session.get_item('user')
        if user_str:
            user = json.loads(user_str)
        else:
            user = {}
        kwargs.update({'username': user.get('username', '')})
        self.render(template, **kwargs)
