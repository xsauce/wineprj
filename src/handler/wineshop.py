# coding:utf-8
import re
import traceback
from bson import ObjectId
from handler.CommonHandler import WineShopCommonHandler
from logiclayer.wineshop import *
from utils.exceptions import OrderIsEmpty, SessionOverTime
from utils.image_tool import get_thumbnail_uri
from utils.mongohelper import MongoHelper
from utils.page_func import tojsonstr

def _show_product_list_with_count(pid_with_count):
    product_list = get_product_with_id_from_db(pid_with_count.keys())
    product_sum_count, product_sum_price = 0, 0
    for p in product_list:
        purchase_count = pid_with_count[p['pid']]
        p['purchase_count'] = purchase_count
        product_sum_price += p['price'] * purchase_count
        product_sum_count += purchase_count
    return product_list, product_sum_count, product_sum_price

class HomeHandler(WineShopCommonHandler):
    def get(self):
        poster_list = get_home_posts_from_db('home')
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
        product_result = query_product_list_from_db(query_condition)
        grape_sort = get_grape_sort_list()
        product_list = []
        for product in product_result:
            if product['img']:
                imgs = product['img'].split(',')
                product['fimg'] = get_thumbnail_uri(imgs[0])
            product_list.append(product)
        self.page_render('wineshop/products.html', product_list=product_list, grape_sort=grape_sort)


class ProductDetailHandler(WineShopCommonHandler):
    def get(self, product_id):
        if product_id:
            db = MongoHelper().connect()
            product = db.product.find_one({'_id': ObjectId(product_id)})
            if not product:
                errmsg = 'not found product %s in ProductDetailHanlder' % product_id
                self.logger.error(errmsg)
                raise Exception(errmsg)
            # comments = db.comment.find({'product_id': prodcut_id})
            comments = None
            delivery_days = 1
            self.page_render('wineshop/product_detail.html', product=product, comments=comments, delivery_days=delivery_days)
        else:
            errmsg = 'invalid parameter in ProductDetailHandler'
            raise Exception(errmsg)


class ShopCarHandler(WineShopCommonHandler):
    def get(self, product_id):
        shopcar = self.get_cookie('shopcar', [])
        shopcar_dict = dict()
        for p in shopcar:
            p_split = p.split(':')
            shopcar_dict[p_split[0]] = int(p_split[1])
        if product_id:
            shopcar_dict[product_id] = shopcar_dict.setdefault(product_id, 0) + 1
        db = MongoHelper().connect()
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
            db = MongoHelper().connect()
            product_list_order, product_sum_count, product_sum_price = _show_product_list_with_count(order)
            ship_cities = get_all_ship_cities_from_db()
            pay_sorts = list(db.pay_sort.find())
            shipping_cost = 5
            self.page_render('wineshop/order.html',
                             product_list_order=product_list_order,
                             product_sum_count=product_sum_count,
                             product_sum_price=product_sum_price,
                             shipping_cost=shipping_cost,
                             ship_cities=ship_cities,
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

    def _valid_post_data(self, post_data, ship_cities, pay_sort):
        field_error = {}
        if post_data['addr_level1'] not in ship_cities.keys():
            field_error['addr_level1'] = u'请选择正确的直辖市或省份'
        else:
            if post_data['addr_level2'] not in ship_cities[post_data['addr_level1']]:
                field_error['addr_level2'] = u'请选择正确的城市或区'
        if not post_data['addr_level3']:
            field_error['addr_level3'] = u'请填写详细地址'

        if post_data['pay_sort'] not in [x['name'] for x in pay_sort]:
            field_error['pay_sort'] = u'请选择正确的支付方式'

        if post_data['receiver'] == '':
            field_error['receiver'] = u'请填写正确的名字'

        if not re.match('\d{11}', post_data['phone']):
            field_error['phone'] = u'请填写正确的手机号'

        valcode = self.session.get_item('valcode', '').upper()
        if valcode != '':
            raise SessionOverTime()
        if valcode == post_data['valcode'].upper():
            field_error['valcode'] = u'验证码错误'

        if post_data['need_receipt']:
            receipt_sort = post_data['receipt_sort']
            if not receipt_sort or receipt_sort not in [u'个人发票', u'公司发票']:
                field_error['receipt_sort'] = u'请选择正确的发票类型'
            if not post_data['receipt_content']:
                field_error['receipt_content'] = u'请选择发票内容'
            if receipt_sort == u'公司发票' and post_data['receipt_title'] == '':
                field_error['receipt_title'] = u'开公司发票,请填写发票抬头'

        try:
            map(int, post_data['order'].values())
        except Exception, e:
            print e
            field_error['order'] = u'请填写正确的购买数量'
        return field_error

    def post(self):
        db = MongoHelper().connect()
        ship_cities = get_all_ship_cities_from_db()
        pay_sorts = list(db.pay_sort.find())
        post_data = self._get_post_data()
        field_error = self._valid_post_data(post_data, ship_cities, pay_sorts)
        product_list_order, product_sum_count, product_sum_price = _show_product_list_with_count(post_data['order'])
        shipping_cost = 5
        if field_error:
            self.page_render('wineshop/order.html',
                             product_list_order=product_list_order,
                             product_sum_count=product_sum_count,
                             product_sum_price=product_sum_price,
                             shipping_cost=shipping_cost,
                             ship_cities=ship_cities,
                             pay_sorts=pay_sorts,
                             tojsonstr=tojsonstr,
                             field_error=field_error,
                             post_data=post_data)
        else:
            #insert order, state:new
            db.order.insert_one({

            })
            #update store count, sale count





