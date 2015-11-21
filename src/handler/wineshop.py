# coding:utf-8
import traceback
from bson import ObjectId
from handler.CommonHandler import WineShopCommonHandler
from utils.exceptions import OrderIsEmpty
from utils.image_tool import get_thumbnail_uri
from utils.mongohelper import MongoHelper
from utils.page_func import tojsonstr


class HomeHandler(WineShopCommonHandler):
    def get(self):
        db = MongoHelper().connect()
        poster_list = db.poster.find({'show_place': 'home'})
        self.page_render('wineshop/home.html', poster_list=poster_list)


class ProductsHandler(WineShopCommonHandler):
    def _build_query_condition(self, query_args):
        condition = {}
        for k, v in query_args.items():
            if v and k in ['brand', 'country', 'area', 'grape_sort', 'scene', 'wine_level']:
                if len(v) == 1 and v[0]:
                    condition[k] = v[0]
                elif len(v) > 1:
                    condition[k] = {'$in': v}
            if v and k == 'price_range':
                if len(v) == 1 and v[0]:
                    price_range = v[0].split(',')
                    condition[k] = {'$gte': price_range[0], '$lte': price_range[1]}
        return condition

    def get(self):
        query_args = self.request.query_arguments
        db = MongoHelper().connect()
        query_condition = self._build_query_condition(query_args)
        product_result = db.product.find(query_condition)
        grape_sort_result = db.product.distinct('grape_sort')
        grape_sort = []
        for sort in grape_sort_result:
            grape_sort.append(sort)
        product_list = []
        for product in product_result:
            for img in product['img']:
                if img['seq'] == 1:
                    product['fimg'] = get_thumbnail_uri(img['uri'])
                    break
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
        product_list_in_shopcar = []
        product_cur = db.product.find({'_id': {'$in': map(ObjectId, shopcar_dict.keys())}})
        product_count_in_shopcar = sum(shopcar_dict.values())
        product_sum_price_in_shopcar = 0
        attachment_ids = set()
        for p in product_cur:
            map(lambda x: attachment_ids.add(x), p['attachment'])
            p['purchase_count'] = int(shopcar_dict.get(p['_id'], 1))
            product_sum_price_in_shopcar += p['purchase_count'] * p['price']
            product_list_in_shopcar.append(p)
        attachment_cur = db.attachment.find({'_id': {'$in': list(attachment_ids)}})
        attachment_dict = {}
        for a in attachment_cur:
            attachment_dict[ObjectId(a['_id'])] = a
        self.page_render('wineshop/shopcar.html',
                         product_list_in_shopcar=product_list_in_shopcar,
                         product_count_in_shopcar=product_count_in_shopcar,
                         product_sum_price_in_shopcar=product_sum_price_in_shopcar,
                         attachment_dict=attachment_dict)


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
            product_list_order = []
            product_cur = db.product.find({'_id': {'$in': map(ObjectId, order.keys())}})
            product_sum_count = sum(order.values())
            product_sum_price = 0
            attachment_ids = set()
            for p in product_cur:
                map(lambda x: attachment_ids.add(x), p['attachment'])
                p['purchase_count'] = int(order.get(p['_id'], 1))
                product_sum_price += p['purchase_count'] * p['price']
                product_list_order.append(p)
            attachment_cur = db.attachment.find({'_id': {'$in': list(attachment_ids)}})
            attachment_dict = {}
            for a in attachment_cur:
                attachment_dict[ObjectId(a['_id'])] = a
            ship_cities = {}
            ship_cities_cur = db.ship_city.find()
            for city in ship_cities_cur:
                city_name = city['name']
                ship_cities[city_name] = []
                for d in city['district']:
                    ship_cities[city_name].append(d['name'])
            pay_sorts = list(db.pay_sort.find())
            shipping_cost = 5
            a = tojsonstr(ship_cities)
            self.page_render('wineshop/confirm_order.html',
                             product_list_order=product_list_order,
                             product_sum_count=product_sum_count,
                             product_sum_price=product_sum_price,
                             shipping_cost=shipping_cost,
                             attachment_dict=attachment_dict,
                             ship_cities=ship_cities,
                             pay_sorts=pay_sorts,
                             tojsonstr=tojsonstr)
        except OrderIsEmpty, e:
            raise e
        except Exception, e:
            errmsg = 'error in ConfirmOrderHandler: name=%s, detail=%s' % (str(e), traceback.format_exc())
            raise Exception(errmsg)

class SubmitOrderHandlder(WineShopCommonHandler):
    def _get_post_data(self):
        post_data = {}
        post_data['addr_level1'] = self.get_body_argument('addr_level1')
        post_data['addr_level2'] = self.get_body_argument('addr_level2')
        post_data['addr_level3'] = self.get_body_argument('addr_level3')
        post_data['receiver'] = self.get_body_argument('receiver')
        post_data['phone'] = self.get_body_argument('phone')
        post_data['receipt_sort'] = self.get_body_argument('receipt_sort')


    def post(self):
        pass




