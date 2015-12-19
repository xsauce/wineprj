# coding: utf-8
from CommonModel import *
from utils.sqlhelper import WHERE_CONDITION

__author__ = 'sam'


class User(CommonModel):
    __tablename__ = 'user'
    __pk__ = 'uid'

    uid = None
    username = None
    password = None
    email = None
    phone = None
    avatar = None
    created_at = None
    updated_at = None


class Administrator(CommonModel):
    __tablename__ = 'administrator'
    __pk__ = 'aid'

    aid = None
    username = None
    password = None
    email = None
    phone = None
    created_at = None
    updated_at = None


class Repertory(CommonModel):
    __tablename__ = 'repertory'
    __pk__ = 'pid'
    pid = None
    sale_count = None
    store_count = None
    created_at = None
    updated_at = None

    @classmethod
    def sale_product(cls, pid, product_count):
        sql = 'update %s set sale_count=sale_count+%s, store_count=store_count-%s where pid=%s' % (
            cls.__tablename__, product_count, product_count, pid
        )
        SqlHelper().execute(sql, {})

    @classmethod
    def sale_product_for_batch(cls, pid_list_with_count):
        '''
        pid_list_with_count:data structure: {'pid': 113213, 'product_count':2 }
        '''
        sql = 'update ' + cls.__tablename__ + ' set sale_count=sale_count+%(product_count)s, store_count=store_count-%(product_count)s where pid=%(pid)s'
        SqlHelper().execute_many(sql, pid_list_with_count)


class RepertoryEntry(CommonModel):
    __tablename__ = 'repertory_entry'
    __pk__ = 'reid'

    reid = None
    pid = None
    entry_count = None
    created_at = None
    updated_at = None


class SaleOrder(CommonModel):
    __tablename__ = 'sale_order'
    __pk__ = 'soid'

    NOPAY = u'未支付'
    PAID = u'已支付'
    HANDLING = u'订单处理'
    DELIVERY = u'商品出库'
    FINISH = u'订单完成'
    CANCEL = u'订单缺消'
    ORDER_STATE_CHOICES = (
        (NOPAY, 0),
        (PAID, 1),
        (HANDLING, 2),
        (DELIVERY, 3),
        (FINISH, 4),
        (CANCEL, 5)
    )

    @classmethod
    def get_order_state_num(cls, choice):
        return cls.choice_digitalize(choice, choice_list_name='ORDER_STATE_CHOICES')
    @classmethod
    def get_order_state_display(cls, num):
        return cls.choice_display(num, choice_list_name='ORDER_STATE_CHOICES')


    soid = None
    uid = None
    addr_level1 = None
    addr_level2 = None
    addr_level3 = None
    shipping_cost = None
    product_sum_price = None
    product_count = None
    receiver = None
    phone = None
    receipt_sort = None
    receipt_content = None
    receipt_title = None
    pay_sort = None
    order_state = None
    created_at = None
    updated_at = None


class SaleOrderDetail(CommonModel):
    __tablename__ = 'sale_order_detail'
    __pk__ = 'sodid'

    sodid = None
    soid = None
    pid = None
    purchase_count = None
    price = None


class SaleOrderTrace(CommonModel):
    __tablename__ = 'sale_order_trace'
    __pk__ = 'sotid'

    sotid = None
    soid = None
    state = None
    created_at = None
    updated_at = None

class ShipCity(CommonModel):
    __tablename__ = 'ship_city'
    __pk__ = 'city_id'

    city_id = None
    name = None
    district = None


class Product(CommonModel):
    __tablename__ = 'product'
    __pk__ = 'pid'

    pid = None
    name = None
    img_url = None
    parent_id = None
    description = None
    volume = None
    price = None
    brand = None
    country = None
    area = None
    grape_sort = None
    scene = None
    wine_level = None
    sort = None
    created_at = None
    updated_at = None


class Poster(CommonModel):
    __tablename__ = 'poster'
    __pk__ = 'poster_id'

    poster_id = None
    description = None
    show_place = None
    seq = None


class PaySort(CommonModel):
    ALIPAY = u'支付宝'
    COD = u'货到付款'
    SORT_CHOICE = (
        (ALIPAY, 1),
        (COD, 2)
    )
    @classmethod
    def get_sort_num(cls, choice):
        return cls.choice_digitalize(choice, choice_list_name='SORT_CHOICE')
    @classmethod
    def get_sort_display(cls, num):
        return cls.choice_display(num, choice_list_name='SORT_CHOICE')







