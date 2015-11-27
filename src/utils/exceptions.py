# coding: utf-8
import settings

__author__ = 'sam'

class NotFoundProduct(Exception):
    def __init__(self, product_id):
        self.product_id = product_id
        super(NotFoundProduct, self).__init__()
    def __str__(self):
        if not settings.DEBUG:
            return u'我家酒窖没有这瓶酒,等我去进货'
        return 'No found Product %s' % self.product_id

class OrderIsEmpty(Exception):
    def __str__(self):
        if not settings.DEBUG:
            return u'购物车里空空的,赶紧买买买'
        return 'Order is Empty'

class SessionOverTime(Exception):
    def __str__(self):
        if not settings.DEBUG:
            return u'系统繁忙,请重新提交订单'
        return 'SessionOverTime'