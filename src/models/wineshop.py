import uuid
from CommonModel import *
__author__ = 'sam'


class User(CommonModel):
    __tablename__ = 'user'
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
    aid = None
    username = None
    password = None
    email = None
    phone = None
    created_at = None
    updated_at = None


class Repertory(CommonModel):
    __tablename__ = 'repertory'
    rid = None
    pid = None
    sale_count = None
    store_count = None
    created_at = None
    updated_at = None


class RepertoryEntry(CommonModel):
    __tablename__ = 'repertory_entry'
    reid = None
    pid = None
    entry_count = None
    created_at = None
    updated_at = None


class SaleOrder(CommonModel):
    __tablename__ = 'sale_order'
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

    soid = None
    uid = None
    addr_level1 = None
    addr_level2 = None
    addr_level3 = None
    shipping_cost = None
    product_sum_price = None
    product_count = None
    receiver = None
    receiver_phone = None
    receipt_sort = None
    receipt_content = None
    receipt_title = None
    pay_sort = None
    order_state = None
    created_at = None
    updated_at = None


class SaleOrderDetail(CommonModel):
    __tablename__ = 'sale_order_detail'
    sodid = None
    soid = None
    pid = None
    purchase_count = None
    price = None


class SaleOrderTrace(CommonModel):
    __tablename__ = 'sale_order_trace'
    sotid = None
    soid = None
    state = None
    created_at = None


class ShipCity(CommonModel):
    __tablename__ = 'ship_city'
    city_id = None
    name = None
    district = None


class Product(CommonModel):
    __tablename__ = 'product'
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

    @classmethod
    def insert_one_product(cls, product):
        product.pid = str(uuid.uuid4())
        insert_fields = product.keys()
        insert_params = cls.to_sql_params(insert_fields)
        sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' %(cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
        SqlHelper().execute(sql, product.__dict__)
        return product.pid

    @classmethod
    def insert_many_product(cls, products):
        pid_list = []
        for p in products:
            p['pid'] = str(uuid.uuid4())
            pid_list.append(p['pid'])
        insert_fields = products[0].keys()
        insert_params = cls.to_sql_param_list(insert_fields)
        sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' %(cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
        SqlHelper().execute_many(sql, [p for p in products])
        return pid_list


class Poster(CommonModel):
    __tablename__ = 'poster'
    poster_id = None
    description = None
    show_place = None
    seq = None

    @classmethod
    def find_by_place(cls, place):
        rs = cls.find(select_fields=cls.all_field(), sql_value={'show_place': place}, where_str='show_place=?show_place', return_obj=True)
        return rs








