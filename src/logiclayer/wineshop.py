# coding:utf-8
import hashlib
from models.wineshop import Product, ShipCity, Poster, PaySort, SaleOrder, SaleOrderDetail, Repertory, SaleOrderTrace, \
    User
from readonly_cache_data import PAY_SORTS, RECEIPT_CONTENT
from utils.sqlhelper import WHERE_CONDITION, TransactionContext


class ProductLL(object):
    @classmethod
    def str_to_array(cls, img_url):
        return img_url.split(',') if img_url else []

    @classmethod
    def query_product_list(cls, query_condition):
        where_str, where_values = '', {}
        if query_condition:
            where_str, where_values = WHERE_CONDITION.build(query_condition)
        product_list = Product.find(where_str=where_str, sql_value=where_values, return_obj=False)
        for p in product_list:
            p['img_url'] = cls.str_to_array(p['img_url'])
        return product_list

    @classmethod
    def get_product_by_pid_list(cls, pid_list):
        where_value, where_str = WHERE_CONDITION.IN('pid', pid_list)
        product_list = Product.find(where_str=where_str, sql_value=where_value, return_obj=False)
        for p in product_list:
            p['img_url'] = cls.str_to_array(p['img_url'])
        return product_list

    @classmethod
    def get_grape_sort_list(cls):
        result = Product.find(select_fields=['distinct grape_sort'])
        grape_sort_list = []
        for d in result:
            grape_sort_list.append(d.grape_sort)
        return grape_sort_list

    @classmethod
    def get_one_by_pid(cls, pid):
        where_value, where_str = WHERE_CONDITION.EXACT('pid', pid)
        rs = Product.find_one(where_str=where_str, sql_value=where_value, return_obj=False)
        if rs:
            rs['img_url'] = cls.str_to_array(rs['img_url'])
        else:
            rs = {}
        return rs

class SaleOrderLL(object):
    @classmethod
    def add_one_order(cls, order, order_detail, user=None):
        if order.pay_sort == PaySort.COD:
            order.state = SaleOrder.get_order_state_num(SaleOrder.HANDLING)
        elif order.pay_sort == PaySort.ALIPAY:
            order.state = SaleOrder.get_order_state_num(SaleOrder.NOPAY)
        product_count = 0
        product_sum_price = 0.0
        for od in order_detail:
            product_count += od.purchase_count
            product_sum_price += od.purchase_count * od.price
        order.product_count = product_count
        order.product_sum_price = product_sum_price
        if user:
            order.uid = user.uid
        with TransactionContext():
            soid = SaleOrder.insert_one_with_created_updated_at_return_pk(order)
            pid_with_count = []
            for od in order_detail:
                od.soid = soid
                pid_with_count.append({'pid': od.pid, 'product_count': od.purchase_count})
            SaleOrderDetail.insert_many_with_return_pk(order_detail)
            Repertory.sale_product_for_batch(pid_with_count)
            trace = SaleOrderTrace({'soid': soid, 'state': order.state})
            SaleOrderTrace.insert_one_with_created_updated_at_return_pk(trace)

class ShipCityLL(object):
    @classmethod
    def district_to_array(cls, row):
        row['district'] = row.get('district', '').decode('utf-8').split(',')

    @classmethod
    def get_all_ship_cities(cls):
        rs = ShipCity.find(select_fields=['name', 'district'], return_obj=False)
        if rs:
            ds = {}
            for r in rs:
                cls.district_to_array(r)
                ds[r['name'].decode('utf-8')] = r['district']
            return ds
        else:
            return {}


class PosterLL(object):
    @classmethod
    def get_poster_by_place(cls, place):
        where_value, where_str = WHERE_CONDITION.EXACT('show_place', place)
        rs = Poster.find(select_fields=Poster.all_field(), sql_value=where_value, where_str=where_str, return_obj=False)
        return rs

class PaySortLL(object):
    @classmethod
    def get_all_sort(cls):
        return PAY_SORTS

class ReceiptLL(object):
    @classmethod
    def get_all_content(cls):
        return RECEIPT_CONTENT


class UserLL(object):
    LLERROR = ''

    @classmethod
    def md5_password(cls, password):
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()

    @classmethod
    def valid_user(cls, login_key, password, locale_func):
        cls.LLERROR = ''
        email_value, email_str = WHERE_CONDITION.EXACT('email', login_key)
        username_value, username_str = WHERE_CONDITION.EXACT('username', login_key)
        sql_value = {}
        sql_value.update(email_value)
        sql_value.update(username_value)
        user = User.find_one(['uid', 'username', 'password'], sql_value, email_str + ' or ' + username_str)
        if user:
            if user.password == cls.md5_password(password):
                user.password = None
                return user
            else:
                UserLL.LLERROR = locale_func('wrong_password')
        else:
            cls.LLERROR = locale_func('no_exist_email_or_user_name')
            return None

    @classmethod
    def add_one_uesr(cls, user, locale_func):
        cls.LLERROR = ''
        where_value, where_str = WHERE_CONDITION.EXACT('email', user.email)
        rs = User.find_one(['uid'], where_value, where_str)
        if rs:
            cls.LLERROR = locale_func('email_is_registered')
            return
        user.password = cls.md5_password(user.password)
        with TransactionContext():
            User.insert_one_with_created_updated_at_return_pk(user)

