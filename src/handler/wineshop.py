# coding:utf-8
import os
from bson import ObjectId
from handler.CommonHandler import CommonHandler
from utils.image_tool import get_thumbnail_uri
from utils.mongohelper import MongoHelper


class HomeHandler(CommonHandler):
    def get(self):
        poster_list = None # get poster.url, poster.description
        self.render('wineshop/home.html', {'poster_list': poster_list})


class ProductsHandler(CommonHandler):
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


class ProductDetailHandler(CommonHandler):
    def get(self, product_id):
        if product_id:
            db = MongoHelper().connect()
            product = db.product.find_one({'_id': ObjectId(product_id)})
            if not product:
                raise Exception('not found product %s in ProductDetailHanlder' % product_id)
            # comments = db.comment.find({'product_id': prodcut_id})
            comments = None
            delivery_days = 1
            self.page_render('wineshop/product_detail.html', product=product, comments=comments, delivery_days=delivery_days)
        else:
            raise Exception('invalid parameter in ProductDetailHandler')


class BuyProductHandler(CommonHandler):
    def get(self, product_id):
        if product_id:
            pass




