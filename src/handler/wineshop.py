# coding:utf-8
import os
from bson import ObjectId
from handler.CommonHandler import WineShopCommonHandler
from utils.image_tool import get_thumbnail_uri
from utils.mongohelper import MongoHelper


class HomeHandler(WineShopCommonHandler):
    def get(self):
        poster_list = None # get poster.url, poster.description
        self.render('wineshop/home.html', {'poster_list': poster_list})


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
            self.logger.error(errmsg)
            raise Exception(errmsg)


class BuyProductHandler(WineShopCommonHandler):
    def get(self, product_id):
        if product_id:
            shopcar = self.get_cookie('shopcar', [])
            shopcar_dict = dict()
            for p in shopcar:
                p_split = p.split(':')
                shopcar_dict[p_split[0]] = int(p_split[1])
            shopcar_dict[product_id] = shopcar_dict.setdefault(product_id, 0) + 1
            db = MongoHelper().connect()
            product_list_in_shopcar = []
            product_cur = db.product.find({'_id': {'$in': map(ObjectId, shopcar_dict.keys())}})
            product_count_in_shopcar = sum(shopcar_dict.values())
            product_sum_price_in_shopcar = 0
            shipping_cost = 5
            attachment_ids = set()
            for p in product_cur:
                map(lambda x: attachment_ids.add(x), p['attachment'])
                p['purchase_count'] = int(shopcar_dict.get(p['_id'], 1))
                product_sum_price_in_shopcar += p['purchase_count'] * p['price']
                product_list_in_shopcar.append(p)
            attachment_cur = db.attachment.find({'_id': {'$in': list(attachment_ids) }})
            attachment_dict = {}
            for a in attachment_cur:
                attachment_dict[ObjectId(a['_id'])] = a
            self.page_render('wineshop/shopcar.html',
                             product_list_in_shopcar=product_list_in_shopcar,
                             product_count_in_shopcar=product_count_in_shopcar,
                             product_sum_price_in_shopcar=product_sum_price_in_shopcar,
                             shipping_cost=shipping_cost, attachment_dict=attachment_dict)
        else:
            self.logger.error('no product_id parameter in BuyProductHandler')
            raise Exception('no product_id parameter in BuyProductHandler')





