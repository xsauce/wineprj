# coding:utf-8
import re
import traceback
from handler.CommonHandler import WineShopCommonHandler
from handler.tools import VALCODE_NAME
from logiclayer.wineshop import *
from utils.exceptions import OrderIsEmpty, SessionOverTime
from utils.image_tool import get_thumbnail_uri
# from utils.mongohelper import MongoHelper
from utils.page_func import tojsonstr

def _show_product_list_with_count(pid_with_count):
    product_list = ProductLL.get_product_by_pid_list(pid_with_count.keys())
    product_sum_count, product_sum_price = 0, 0
    for p in product_list:
        purchase_count = int(pid_with_count[p['pid']])
        p['purchase_count'] = purchase_count
        product_sum_price += p['price'] * purchase_count
        product_sum_count += purchase_count
    return product_list, product_sum_count, product_sum_price

class HomeHandler(WineShopCommonHandler):
    def get(self):
        poster_list = PosterLL.get_poster_by_place('home')
        self.page_render('wineshop/home.html', poster_list=poster_list)


class ProductsHandler(WineShopCommonHandler):
    def _build_query_condition(self, query_args):
        condition = []
        for k, v in query_args.items():
            if v and k in ['brand', 'country', 'area', 'grape_sort', 'scene', 'wine_level']:
                if len(v) == 1 and v[0]:
                    condition.append((k, v[0], WHERE_CONDITION.EXACT))
                elif len(v) > 1:
                    condition.append((k, v, WHERE_CONDITION.IN))
            if v and k == 'price_range':
                if len(v) == 1 and v[0]:
                    price_range = v[0].split(',')
                    condition.append((k, price_range, WHERE_CONDITION.RANGE))
        return condition

    def get(self):
        query_args = self.request.query_arguments
        query_condition = self._build_query_condition(query_args)
        product_result = ProductLL.query_product_list(query_condition)
        grape_sort = ProductLL.get_grape_sort_list()
        product_list = []
        for product in product_result:
            if product['img_url']:
                product['fimg'] = product['img_url'][0]
            product_list.append(product)
        self.page_render('wineshop/products.html', product_list=product_list, grape_sort=grape_sort)


class ProductDetailHandler(WineShopCommonHandler):
    def get(self, product_id):
        if product_id:
            product = ProductLL.get_one_by_pid(product_id)
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
    def get(self, product_id):
        shopcar = self._get_shopcar_cookie()
        shopcar_dict = dict()
        for p in shopcar:
            p_split = p.split(':')
            pid = p_split[0]
            if len(p_split) == 2:
                shopcar_dict[pid] = shopcar_dict.setdefault(pid, 0) + int(p_split[1])
            else:
                shopcar_dict[pid] = shopcar_dict.setdefault(pid, 0) + 1
        if product_id:
            shopcar_dict[product_id] = shopcar_dict.setdefault(product_id, 0) + 1
        product_list_in_shopcar, product_count_in_shopcar, product_sum_price_in_shopcar = _show_product_list_with_count(shopcar_dict)
        self.page_render('wineshop/shopcar.html',
                         product_list_in_shopcar=product_list_in_shopcar,
                         product_count_in_shopcar=product_count_in_shopcar,
                         product_sum_price_in_shopcar=product_sum_price_in_shopcar)


class ConfirmOrderHandler(WineShopCommonHandler):
    def post(self):
        order = {}
        try:
            pids_in_shopcar = self.get_body_arguments('product_id_list_in_shopcar')
            for i in pids_in_shopcar:
                order[i] = int(self.get_body_argument('product-%s-purchase_count' % i))
            if not order:
                #order is empty
                raise OrderIsEmpty()
            product_list_order, product_sum_count, product_sum_price = _show_product_list_with_count(order)
            ship_cities = ShipCityLL.get_all_ship_cities()
            pay_sorts = PaySortLL.get_all_sort()
            receipt_content = ReceiptLL.get_all_content()
            shipping_cost = 5
            self.page_render('wineshop/order.html',
                             product_list_order=product_list_order,
                             product_sum_count=product_sum_count,
                             product_sum_price=product_sum_price,
                             shipping_cost=shipping_cost,
                             ship_cities=ship_cities,
                             receipt_content=receipt_content,
                             pay_sorts=pay_sorts,
                             field_error={},
                             post_data={},
                             tojsonstr=tojsonstr)
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

    def _valid_post_data(self, post_data, ship_cities, pay_sort, receipt_content):
        field_error = {}
        if post_data['addr_level1'] not in ship_cities.keys():
            field_error['addr_level1'] = u'请选择正确的直辖市或省份'
        else:
            if post_data['addr_level2'] not in ship_cities[post_data['addr_level1']]:
                field_error['addr_level2'] = u'请选择正确的城市或区'
        if not post_data['addr_level3']:
            field_error['addr_level3'] = u'请填写详细地址'

        if post_data['pay_sort'] not in pay_sort:
            field_error['pay_sort'] = u'请选择正确的支付方式'

        if post_data['receiver'] == '':
            field_error['receiver'] = u'请填写正确的名字'

        if not re.match('\d{11}', post_data['phone']):
            field_error['phone'] = u'请填写正确的手机号'

        valcode = self.session.get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode != post_data['valcode'].upper():
            field_error['valcode'] = u'验证码错误'

        if post_data['need_receipt']:
            receipt_sort = post_data['receipt_sort']
            if not receipt_sort or receipt_sort not in [u'个人发票', u'公司发票']:
                field_error['receipt_sort'] = u'请选择正确的发票类型'
            if not post_data['receipt_content']:
                field_error['receipt_content'] = u'请选择发票内容'
            elif post_data['receipt_content'] not in receipt_content:
                field_error['receipt_content'] = u'请选择正确的发票内容'
            if receipt_sort == u'公司发票' and post_data['receipt_title'] == '':
                field_error['receipt_title'] = u'开公司发票,请填写发票抬头'

        try:
            map(int, post_data['order'].values())
        except Exception, e:
            print e
            field_error['order'] = u'请填写正确的购买数量'
        return field_error

    def post(self):
        ship_cities = ShipCityLL.get_all_ship_cities()
        pay_sorts = PaySortLL.get_all_sort()
        receipt_content = ReceiptLL.get_all_content()
        post_data = self._get_post_data()
        field_error = self._valid_post_data(post_data, ship_cities, pay_sorts, receipt_content)
        product_list_order, product_sum_count, product_sum_price = _show_product_list_with_count(post_data['order'])
        shipping_cost = 5
        if field_error:
            self.page_render('wineshop/order.html',
                             product_list_order=product_list_order,
                             product_sum_count=product_sum_count,
                             product_sum_price=product_sum_price,
                             shipping_cost=shipping_cost,
                             ship_cities=ship_cities,
                             receipt_content=receipt_content,
                             pay_sorts=pay_sorts,
                             tojsonstr=tojsonstr,
                             field_error=field_error,
                             post_data=post_data)
        else:
            order_detail = []
            for p in product_list_order:
                sod = SaleOrderDetail()
                sod.pid = p['pid']
                sod.purchase_count = int(post_data['order'][sod.pid])
                sod.price = p['price']
                order_detail.append(sod)
            order = SaleOrder(post_data)
            order.shipping_cost = 5
            SaleOrderLL.add_one_order(order, order_detail)
            if order.pay_sort == PaySort.ALIPAY:
                pass
            elif order.pay_sort == PaySort.COD:
                self.page_render('wineshop/tip.html', tip=u'订单提交成功!')

class LoginUserForm(object):
    login_key = None
    password = None
    vcode = None

    def __init__(self, post_dict):
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
        user = UserLL.valid_user(self.login_key, self.password)
        if UserLL.LLERROR:
            errors['all'] = UserLL.LLERROR
        valcode = handler.session.get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode != self.vcode.upper():
            errors['vcode'] = u'验证码错误'
        return errors, user

class RegisterUserForm(object):
    email = None
    password = None
    repeat_password = None
    username = None
    vcode = None
    username = None

    def __init__(self, post_dict):
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
            errors['email'] = u'填写正确的邮箱'
        if not self.password:
            errors['password'] = u'请填写密码'
        elif self.password != self.password:
            errors['repeat_password'] = u'两次填写的密码不一致'
        if not self.username:
            errors['username'] = u'请填写用户名'
        valcode = handler.session.get_item(VALCODE_NAME, '').upper()
        if valcode == '':
            raise SessionOverTime()
        if valcode !=self.vcode.upper():
            errors['vcode'] = u'验证码错误'
        return errors

class LoginUserHandler(WineShopCommonHandler):

    def get(self):
        self.page_render('wineshop/login.html', errors={}, post_data={})
    def post(self):
        login_form = LoginUserForm(self.request.body_arguments)
        errors, user = login_form.valid(self)
        if errors:
            self.page_render('wineshop/login.html', errors=errors, post_data=login_form.__dict__)
        else:
            self.session.set_item('user', tojsonstr(user.__dict__))
            self.page_render('wineshop/tip.html', tip='登陆成功')


class RegisterUserHandler(WineShopCommonHandler):
    def get(self):
        self.page_render('wineshop/register.html', errors={}, post_data={})

    def post(self):
        register_form = RegisterUserForm(self.request.body_arguments)
        errors = register_form.valid(self)
        if errors:
            self.page_render('wineshop/register.html', errors=errors, post_data=register_form.__dict__)
        else:
            user = User(register_form.__dict__)
            UserLL.add_one_uesr(user)
            if UserLL.LLERROR == '':
                self.page_render('wineshop/tip.html', tip=u'注册成功')
            else:
                errors['all'] = UserLL.LLERROR
                self.page_render('wineshop/register.html', errors=errors, post_data=register_form.__dict__)






