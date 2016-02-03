# coding:utf-8
import hashlib
import uuid
from peewee import fn
from const import *
from logiclayer.helper import return_json
from models.CommonModel import m2d, DB
from models.wineshop import Poster, PaySort, ReceiptContent, Product, ProductPhoto, User, OrderState, SaleOrder, \
    SaleOrderDetail, ShipCity, GrapeSort, Scene, ProductLabel, Country, Brand, Region, WineSort, WineLevel
from utils.image_tool import get_thumbnail_uri


class ProductLL(object):
    def _query_statement(self, k, v):
        return getattr(Product, k) == v

    def _format_product_to_show(self, p, only_show_first_photo=False):
        p.country = Country.get_display(p.country)
        p.brand = Brand.get_display(p.brand)
        p.region = Region.get_display(p.region)
        p.grape_sort = GrapeSort.get_display(p.grape_sort)
        p.sort = WineSort.get_display(p.sort)
        p.wine_level = WineLevel.get_display(p.wine_level)
        dp = m2d(p)
        if only_show_first_photo:
            # just show first photo
            img = p.photos.where(ProductPhoto.seq_num == 1)[0]
            dp['img_url'] = img.hash_value + '.' + img.photo_type
        else:
            img = p.photos
            dp['img_url'] = [i.hash_value + '.' + i.photo_type for i in img]
        scenes = p.scenes
        labels = p.labels
        dp['scenes'] = [Scene.get_display(i.scene) for i in scenes]
        dp['labels'] = [ProductLabel.get_display(i.label) for i in labels]
        return dp

    def query_product_list(self, query_condition):
        '''
        :param query_condition: dict type
        :return:
        '''
        where_condition = 1
        if query_condition:
            for k, v in query_condition.items():
                where_condition = where_condition & self._query_statement(k, v)
        result = Product.select().where(where_condition)
        product_list = []
        for p in result:
            dp = self._format_product_to_show(p, only_show_first_photo=True)
            product_list.append(dp)
        return product_list

    def get_product_by_pid_list(self, pid_list):
        '''
        :param pid_list: list type
        :return:
        '''
        result = Product.select().where(Product.pid << pid_list)
        product_list = []
        for p in result:
            dp = self._format_product_to_show(p)
            product_list.append(dp)
        return product_list

    def get_grape_sort_list(self):
        grape_sort_list = GrapeSort.select()
        return grape_sort_list

    def get_one_by_pid(self, pid):
        p = Product.select().where(Product.pid == pid)
        if not p:
            return {}
        dp = self._format_product_to_show(p[0])
        return dp


class SaleOrderLL(object):
    def add_one_order(self, order, order_detail, user=None):
        o_obj = SaleOrder(**order)
        od_obj_list = []
        for od in order_detail:
            od_obj_list.append(SaleOrderDetail(**od))
        user_obj = None
        if user:
            user_obj = User(user)
        if o_obj.pay_sort == PaySort.get_value(COD):
            o_obj.state = OrderState.get_value(HANDLING)
        elif o_obj.pay_sort == PaySort.get_value(ALIPAY):
            o_obj.state = OrderState.get_value(NOPAY)
        product_count = 0
        product_sum_price = 0.0
        for odb in od_obj_list:
            product_count += odb.purchase_count
            product_sum_price += odb.purchase_count * odb.price
        o_obj.product_count = product_count
        o_obj.product_sum_price = product_sum_price
        if user_obj:
            o_obj.user = user_obj
        with DB.execution_context():
            o_obj.soid = str(uuid.uuid4())
            o_obj.save()
            pid_with_count = []
            for odb in od_obj_list:
                odb.sale_order = o_obj
                pid_with_count.append({'pid': od.pid, 'product_count': od.purchase_count})
                odb.save()
            Repertory.sale_product_for_batch(pid_with_count)
            trace = SaleOrderTrace({'soid': soid, 'state': order.state})
            SaleOrderTrace.insert_one_with_created_updated_at_return_pk(trace)


class ShipCityLL(object):
    def get_all_ship_cities(self):
        rs = ShipCity.select()
        return rs


class PosterLL(object):
    def get_recommend_poster(self):
        return self._get_poster_by_place(RECOMMEND)

    def get_home_poster(self):
        return self._get_poster_by_place(HOME)

    def _get_poster_by_place(self, place):
        rs = Poster.select().where(Poster.place == place)
        return m2d(rs)


class PaySortLL(object):
    def get_all_sort(self):
        return PaySort.select()


class ReceiptLL(object):
    def get_all_content(self):
        return ReceiptContent.select()


class UserLL(object):
    def __init__(self):
        self.error = []

    def _md5_password(self, password):
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()

    @return_json
    def valid_user(self, login_key, password):
        user = User.select().where(User.email == login_key | User.username == login_key)
        if user:
            if user.password == self._md5_password(password):
                user.password = None
                return user
            else:
                self.error.append('wrong_password')
        else:
            self.error.append('no_exist_email_or_user_name')

    def add_one_user(self, user):
        rs = User.select().where(User.email == user.get('email'))
        if rs:
            self.error.append('email_is_registered')
            return 0
        user.password = self._md5_password(user.get('password'))
        with DB.execution_context():
            User.create(**user)
        return 1
