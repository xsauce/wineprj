# coding:utf-8
from tornado.web import url
from handler.wineshop import *
from handler.test import TestHandler

__author__ = 'sam'

url_routes = [
        url(r'/test$', TestHandler, name='test'),
        url(r"^/$", HomeHandler, name='home'),
        url(r"^/products$", ProductsHandler, name='products'),
        url(r"^/product_detail/([\d\w-]+)$", ProductDetailHandler, name='product_detail'),
        url(r"^/buy_product/([\d\w-]+)$", BuyProductHandler, name='buy_product'),
    ]