# coding: utf-8
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
    @property
    def session(self):
        session_id = self.get_secure_cookie(COOKIE_SESSION_NAME)
        if self._session is None:
            self._session = Session(session_id=session_id)
        return self._session

    def create_session_and_set_item(self, key, value, expiry_days=settings.COOKIE_EXPIRY_DAYS):
        self._session = Session()
        self.session.set_item(key, value)
        self.set_secure_cookie(COOKIE_SESSION_NAME, self._session.session_id, expires_days=expiry_days)


class WineShopCommonHandler(CommonHandler):
    def _get_errmsg(status_code):
        if status_code == '404':
            return u'您访问的页面没有找到'
        elif status_code == '500':
            return u'系统正忙，稍后重试'

    def write_error(self, status_code, **kwargs):
        self.logger.error('status_code:%s, errmsg:%s' % (status_code, kwargs))
        if settings.DEBUG:
            errmsg = 'status_code:' + str(status_code) + ',' + unicode(kwargs)
        else:
            errmsg = self._get_errmsg(status_code)
        self.page_render('wineshop/tip.html', tip=errmsg)

    def page_render(self, template, **kwargs):
        kwargs.update({'count_in_shopcar': 1})
        self.render(template, **kwargs)