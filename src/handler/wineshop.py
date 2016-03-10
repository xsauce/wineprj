# coding:utf-8
from functools import partial
import re
import traceback
from handler.CommonHandler import WineShopCommonHandler
from handler.tools import VALCODE_NAME
from logiclayer.wineshop import *
from utils.exceptions import OrderIsEmpty, SessionOverTime
from utils.image_tool import get_thumbnail_uri
# from utils.mongohelper import MongoHelper
from utils.page_func import tojsonstr, address_to_display_json


def _show_product_list_with_count(pid_with_count):
    product_ll = ProductLL()
    product_list = product_ll.get_product_by_pid_list(pid_with_count.keys())
    product_sum_count, product_sum_price = 0, 0
    for p in product_list:
        purchase_count = int(pid_with_count[p['pid']])
        p['purchase_count'] = purchase_count
        product_sum_price += p['price'] * purchase_count
        product_sum_count += purchase_count
    return product_list, product_sum_count, product_sum_price


class HomeHandler(WineShopCommonHandler):
    def get(self):
        poster_list = PosterLL().get_home_poster()
        self.page_render('wineshop/home.html', poster_list=poster_list)


class ProductsHandler(WineShopCommonHandler):
    def _build_query_condition(self, query_args):
        condition = {}
        for k, v in query_args.items():
            if v and k in ['brand', 'country', 'area', 'grape_sort', 'scene', 'wine_level']:
                if len(v) == 1 and v[0]:
                    condition[k] = v[0]
                elif len(v) > 1:
                    condition[k] = v
            if v and k == 'price_range':
                if len(v) == 1 and v[0]:
                    price_range = v[0].split(',')
                    condition[k] = price_range
        return condition

    def get(self):
        query_args = self.request.query_arguments
        query_condition = self._build_query_condition(query_args)
        product_result = ProductLL().query_product_list(query_condition)
        grape_sort = ProductLL().get_grape_sort_list()
        product_list = []
        for product in product_result:
            product_list.append(product)
        self.page_render('wineshop/products.html', product_list=product_list, grape_sort=grape_sort, query_condition=query_condition)


class ProductDetailHandler(WineShopCommonHandler):
    def get(self, product_id):
        if product_id:
            product = ProductLL().get_one_by_pid(product_id)
            if not product:
                errmsg = 'not found product %s in ProductDetailHanlder' % product_id
                self.logger.error(errmsg)
                raise Exception(errmsg)
            # comments = db.comment.find({'product_id': prodcut_id})
            comments = None
            delivery_days = 1
            self.page_render('wineshop/product_detail.html',
                             get_thumbnail_uri=get_thumbnail_uri,
                             product=product,
                             comments=comments,
                             delivery_days=delivery_days)
        else:
            errmsg = 'invalid parameter in ProductDetailHandler'
            raise Exception(errmsg)


class ShopCarHandler(WineShopCommonHandler):
    def _show_page(self, post_data=None):
        shopcar = self._get_shopcar_cookie()
        shopcar_dict = dict()
        for p in shopcar:
            p_split = p.split(':')
            pid = p_split[0]
            if len(p_split) == 2:
                shopcar_dict[pid] = shopcar_dict.setdefault(pid, 0) + int(p_split[1])
            else:
                shopcar_dict[pid] = shopcar_dict.setdefault(pid, 0) + 1
        if post_data:
            product_id = post_data.get('pid', '')
            if product_id:
                shopcar_dict[product_id] = shopcar_dict.setdefault(product_id, 0) + int(
                    self.get_body_argument('purchase_count', 0))
        product_list_in_shopcar, product_count_in_shopcar, product_sum_price_in_shopcar = _show_product_list_with_count(
                shopcar_dict)
        self.page_render('wineshop/shopcar.html',
                         product_list_in_shopcar=product_list_in_shopcar,
                         product_count_in_shopcar=product_count_in_shopcar,
                         product_sum_price_in_shopcar=product_sum_price_in_shopcar)

    def get(self):
        self._show_page()

    def post(self):
        self._show_page(post_data=self.request.body_arguments)


class OrderView(object):
    def __init__(self, handler):
        self.handler = handler

    def render(self, order, field_error, post_data):
        product_list_order, product_sum_count, product_sum_price = _show_product_list_with_count(order)
        ship_cities = ShipCityLL().get_all_ship_cities()
        pay_sorts = PaySortLL().get_all_sort()
        receipt_content = ReceiptLL().get_all_content()
        receipt_sort = ReceiptLL().get_all_sort()
        shipping_cost = 5
        self.handler.page_render('wineshop/order.html',
                         product_list_order=product_list_order,
                         product_sum_count=product_sum_count,
                         product_sum_price=product_sum_price,
                         shipping_cost=shipping_cost,
                         ship_cities=ship_cities,
                         receipt_content=receipt_content,
                         receipt_sort=receipt_sort,
                         pay_sorts=pay_sorts,
                         field_error=field_error,
                         post_data=post_data,
                         address_to_display_str=partial(address_to_display_json, _ul=self.handler._ul))

class ConfirmOrderHandler(WineShopCommonHandler):
    def post(self):
        order = {}
        try:
            pids_in_shopcar = self.get_body_arguments('product_id_list_in_shopcar')
            for i in pids_in_shopcar:
                order[i] = int(self.get_body_argument('product-%s-purchase_count' % i))
            if not order:
                # order is empty
                raise OrderIsEmpty()
            order_view = OrderView(self)
            order_view.render(order, {}, {})
        except OrderIsEmpty, e:
            raise e
        except Exception, e:
            errmsg = 'error in ConfirmOrderHandler: name=%s, detail=%s' % (str(e), traceback.format_exc())
            raise Exception(errmsg)


class SubmitOrderHandlder(WineShopCommonHandler):
    def _get_post_data(self):
        post_data = {}
        post_data['addr_level1'] = self.get_body_argument('addr_level1', '')
        post_data['addr_level2'] = self.get_body_argument('addr_level2', '')
        post_data['addr_level3'] = self.get_body_argument('addr_level3', '')
        post_data['receiver'] = self.get_body_argument('receiver', '')
        post_data['phone'] = self.get_body_argument('phone', '')
        post_data['need_receipt'] = self.get_body_argument('need_receipt', '')
        post_data['receipt_sort'] = self.get_body_argument('receipt_sort', '')
        post_data['receipt_content'] = self.get_body_argument('receipt_content', '')
        post_data['receipt_title'] = self.get_body_argument('receipt_title', '')
        post_data['valcode'] = self.get_body_argument('valcode', '')
        post_data['pay_sort'] = self.get_body_argument('pay_sort', '')
        order = {}
        pids_in_shopcar = self.get_body_arguments('product_id_list_in_order', [])
        for i in pids_in_shopcar:
            order[i] = self.get_body_argument('product-%s-purchase_count' % i, '')
        post_data['order'] = order
        return post_data

    def _valid_post_data(self, post_data):
        field_error = {}
        ship_city_ll = ShipCityLL()
        pay_sort_ll = PaySortLL()
        receipt_ll = ReceiptLL()
        if post_data['addr_level1'] not in ship_city_ll.get_addr_level1_val_list():
            field_error['addr_level1'] = self._ul('incorrect_city')
        else:
            if post_data['addr_level2'] not in ship_city_ll.get_addr_level2_val_list(post_data['addr_level1']):
                field_error['addr_level2'] = self._ul('incorrect_district')
        if not post_data['addr_level3']:
            field_error['addr_level3'] = self._ul('empty_address_detail')

        if post_data['pay_sort'] not in pay_sort_ll.get_val_list():
            field_error['pay_sort'] = self._ul('incorrect_pay_sort')

        if post_data['receiver'] == '':
            field_error['receiver'] = self._ul('incorrect_name')

        if not re.match('\d{11}', post_data['phone']):
            field_error['phone'] = self._ul('incorrect_phone')

        valcode = self.get_session().get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode != post_data['valcode'].upper():
            field_error['valcode'] = self._ul('wrong_valcode')

        if post_data['need_receipt']:
            receipt_sort = post_data['receipt_sort']
            if receipt_sort not in receipt_ll.get_sort_val_list():
                field_error['receipt_sort'] = self._ul('incorrect_receipt_sort')
            if not post_data['receipt_content']:
                field_error['receipt_content'] = self._ul('choose_receipt_content')
            elif post_data['receipt_content'] not in receipt_ll.get_content_val_list():
                field_error['receipt_content'] = self._ul('incorrect_receipt_content')
            if receipt_sort == receipt_ll.sort_value(COMPANY_RECEIPT) and post_data['receipt_title'] == '':
                field_error['receipt_title'] = self._ul('empty_receipt_ title')

        try:
            for k, v in post_data['order'].items():
                post_data['order'][k] = int(v)
        except Exception, e:
            field_error['order'] = self._ul('incorrect_purchase_count')
        return field_error

    def post(self):
        post_data = self._get_post_data()
        field_error = self._valid_post_data(post_data)
        if field_error:
            order_view = OrderView(self)
            order_view.render(post_data['order'], field_error, post_data)
        else:
            sale_order_ll = SaleOrderLL()
            post_data['shipping_cost'] = 5
            sale_order_ll.add_one_order(post_data, self.get_current_user())
            if sale_order_ll.err:
                self.page_render('wineshop/tip.html', tip=str(sale_order_ll.err))
            else:
                pay_sort_ll = PaySortLL()
                if post_data['pay_sort'] == pay_sort_ll.value(ALIPAY):
                    # redirect to alipay page
                    self.page_render('wineshop/tip.html', tip=self._ul(REDIRECTING_TO_ALIPY_PAGE))
                elif post_data['pay_sort'] == pay_sort_ll.value(COD):
                    self.page_render('wineshop/tip.html', tip=self._ul(SUBMIT_ORDER_SUCCESSFULLY))


class LoginUserForm(object):
    login_key = None
    password = None
    vcode = None

    def __init__(self, post_dict, locale_func):
        self.locale_func = locale_func
        for k, v in post_dict.items():
            try:
                if len(v) == 1:
                    setattr(self, k, v[0])
                else:
                    setattr(self, k, v)
            except:
                pass

    def valid(self, handler):
        errors = {}
        user_ll = UserLL()
        user = user_ll.valid_user(self.login_key, self.password)
        if user_ll.error:
            errors['all'] = ','.join([self.locale_func(err) for err in user_ll.error])
        valcode = handler.get_session().get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode != self.vcode.upper():
            errors['vcode'] = self.locale_func('wrong_valcode')
        return errors, user


class RegisterUserForm(object):
    email = None
    password = None
    repeat_password = None
    username = None
    vcode = None

    def __init__(self, post_dict, locale_func):
        self.locale_func = locale_func
        for k, v in post_dict.items():
            try:
                if len(v) == 1:
                    setattr(self, k, v[0])
                else:
                    setattr(self, k, v)
            except:
                pass

    def valid(self, handler):
        errors = {}
        email_match = re.match('^\w+(\.\w+)*@(\w)+(\.\w+)+$', self.email)
        if not email_match:
            errors['email'] = self.locale_func('wrong_email')
        if not self.password:
            errors['password'] = self.locale_func('empty_password')
        elif self.password != self.password:
            errors['repeat_password'] = self.locale_func('passwords_type_twice_not_match')
        if not self.username:
            errors['username'] = self.locale_func('empty_user_name')
        valcode = handler.get_session().get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode != self.vcode.upper():
            errors['vcode'] = self.locale_func('wrong_valcode')
        return errors


class LoginUserHandler(WineShopCommonHandler):
    def get(self):
        self.page_render('wineshop/login.html', errors={}, post_data={})

    def post(self):
        login_form = LoginUserForm(self.request.body_arguments, self._ul)
        errors, user = login_form.valid(self)
        if errors:
            self.page_render('wineshop/login.html', errors=errors, post_data=login_form.__dict__)
        else:
            self.get_session().set_item('user', user)
            self.page_render('wineshop/tip.html', tip=self._ul('login_successfully'))


class RegisterUserHandler(WineShopCommonHandler):
    def get(self):
        self.page_render('wineshop/register.html', errors={}, post_data={})

    def post(self):
        register_form = RegisterUserForm(self.request.body_arguments, self._ul)
        errors = register_form.valid(self)
        if errors:
            self.page_render('wineshop/register.html', errors=errors, post_data=register_form.__dict__)
        else:
            user = register_form.__dict__
            user_ll = UserLL()
            user_ll.add_one_user(user)
            if user_ll.error:
                errors['all'] = ','.join([self._ul(err) for err in user_ll.error])
                self.page_render('wineshop/register.html', errors=errors, post_data=register_form.__dict__)
            else:
                self.page_render('wineshop/tip.html', tip=self._ul('register_successfully'))
