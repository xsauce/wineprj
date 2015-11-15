# coding: utf-8
from tornado.web import RequestHandler
import settings


class CommonHandler(RequestHandler):
    def write_error(self, status_code, **kwargs):
        errmsg = ''
        if settings.DEBUG:
            errmsg = 'status_code:' + str(status_code) + ',' + unicode(kwargs)
        else:
            errmsg = get_errmsg(status_code)
        self.page_render('wineshop/tip.html', tip=errmsg)

    def page_render(self, template, **kwargs):
        kwargs.update({'count_in_shopcar': 1})
        self.render(template, **kwargs)

def get_errmsg(status_code):
    if status_code == '404':
        return u'您访问的页面没有找到'
    elif status_code == '500':
        return u'系统正忙，稍后重试'