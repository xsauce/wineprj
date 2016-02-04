# coding:utf-8
import hashlib
import uuid
from peewee import fn
from const import *
from logiclayer.helper import return_json
from models.CommonModel import m2d, DB
from models.wineshop import Poster, PaySort, ReceiptContent, Product, ProductPhoto, User, OrderState, SaleOrder, \
    SaleOrderDetail, ShipCity, GrapeSort, Scene, ProductLabel, Country, Brand, Region, WineSort, WineLevel, ReceiptSort, \
    SaleOrderTrace, Repertory
from utils.exceptions import NoEnoughStore, NoProductInRepertory


class OrderStateLL(object):
    def value(self, display):
        return OrderState.get_value(display)

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

    def get_product_obj_by_pid_list(self, pid_list):
        return Product.select().where(Product.pid << pid_list)

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
    def __init__(self):
        self.err = {}

    def add_one_order(self, order_data, user):
        order_detail_data = order_data['order']
        order_obj = SaleOrder(
            soid=str(uuid.uuid4()),
            addr_level1=order_data['addr_level1'],
            addr_level2=order_data['addr_level2'],
            addr_level3=order_data['addr_level3'],
            shipping_cost=order_data['shipping_cost'],
            receiver=order_data['receiver'],
            phone=order_data['phone'],
            receipt_sort=order_data['receipt_sort'],
            receipt_content=order_data['receipt_content'],
            receipt_title=order_data['receipt_title'],
            pay_sort=order_data['pay_sort']
        )
        if user:
            order_obj.user = User(**user)
        pay_sort_ll = PaySortLL()
        order_state_ll = OrderStateLL()
        if order_obj.pay_sort == pay_sort_ll.value(COD):
            order_obj.order_state = order_state_ll.value(HANDLING)
        elif order_obj.pay_sort == pay_sort_ll.value(ALIPAY):
            order_obj.order_state = order_state_ll.value(NOPAY)
        product_ll = ProductLL()
        product_details = product_ll.get_product_obj_by_pid_list(order_detail_data.keys())
        order_detail_obj = []
        product_count = 0
        product_sum_price = 0.0
        for pd in product_details:
            sod = SaleOrderDetail(
                sod_id=str(uuid.uuid4()),
                sale_order=order_obj,
                product=pd,
                purchase_count=order_detail_data[pd.pid],
                price=pd.price
            )
            product_count += sod.purchase_count
            product_sum_price += sod.purchase_count * sod.price
            order_detail_obj.append(sod)
        order_obj.product_count = product_count
        order_obj.product_sum_price = product_sum_price
        trace = SaleOrderTrace(
            sot_id=str(uuid.uuid4()),
            sale_order=order_obj,
            state=order_obj.order_state
        )
        reper_ll = RepertoryLL()
        product_reper_list = reper_ll.product_repertory_by_pid_list(order_detail_data.keys())
        with DB.transaction() as trans:
            try:
                for order_detail in order_detail_obj:
                    product = order_detail.product
                    product_reper_list = filter(lambda x: x.product.pid == product.pid, product_reper_list)
                    if not product_reper_list:
                        product_reper = Repertory(
                            product=product
                        )
                        # raise NoProductInRepertory(pid)
                    else:
                        product_reper = product_reper_list[0]
                        # if product_reper.store_count < order_detail.purchase_count:
                        #     raise NoEnoughStore(product.pid)
                    product_reper.sale_count += order_detail.purchase_count
                    product_reper.store_count -= order_detail.purchase_count
                    product_reper.save()
                order_obj.save()
                for d in order_detail_obj:
                    d.save()
                trace.save()
                trans.commit()
            except NoProductInRepertory as e:
                self.err[e.product_id] = str(e)
                trans.rollback()
            except NoEnoughStore as e:
                self.err[e.product_id] = str(e)
                trans.rollback()
            except Exception, e:
                self.err['all'] = str(e)
                trans.rollback()

class RepertoryLL(object):
    def product_repertory_by_pid_list(self, pids):
        products = [Product(pid=pid) for pid in pids]
        return Repertory.select().where(Repertory.product << products)


class ShipCityLL(object):
    def get_all_ship_cities(self):
        rs = ShipCity.select()
        return rs

    def get_addr_level1_val_list(self):
        rs = ShipCity.select()
        return [d['value'] for d in rs]

    def get_addr_level2_val_list(self, addr_level1):
        rs = ShipCity.select()
        city = filter(lambda x: x['value'] == addr_level1, rs)
        if city:
            city = city[0]
            return [d['value'] for d in city['children']]
        else:
            return []


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

    def get_val_list(self):
        return PaySort.value_list()

    def value(self, display):
        return PaySort.get_value(display)



class ReceiptLL(object):
    def get_all_content(self):
        return ReceiptContent.select()

    def get_all_sort(self):
        return ReceiptSort.select()

    def sort_value(self, display):
        return ReceiptSort.get_value(display)

    def get_content_val_list(self):
        return ReceiptContent.value_list()

    def get_sort_val_list(self):
        return ReceiptSort.value_list()


class UserLL(object):
    def __init__(self):
        self.error = []

    def _md5_password(self, password):
        md5 = hashlib.md5()
        md5.update(password)
        return md5.hexdigest()

    @return_json
    def valid_user(self, login_key, password):
        user = User.get(User.email == login_key | User.username == login_key)
        if user:
            if user.password == self._md5_password(password):
                user.password = ''
                user.created_at = ''
                user.updated_at = ''
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
        user['password'] = self._md5_password(user.get('password'))
        user['uid'] = str(uuid.uuid4())
        User.create(**user)
        return 1
