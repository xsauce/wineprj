# coding:utf-8
from tornado.web import url
from handler.wineshop import *
from handler.tools import *
from handler.test import TestHandler

__author__ = 'sam'


url_routes = [
        url(r'/test$', TestHandler, name='test'),
        url(r"^/$", HomeHandler, name='home'),
        url(r"^/products$", ProductsHandler, name='products'),
        url(r"^/product_detail/([\d\w-]+)$", ProductDetailHandler, name='product_detail'),
        url(r"^/shopcar", ShopCarHandler, name='shopcar'),
        url(r"^/confirm_order$", ConfirmOrderHandler, name='confirm_order'),
        url(r'^/verify_code$', VerificationCodeHandler, name='verfiy_code'),
        url(r'^/submit_order$', SubmitOrderHandlder, name='submit_order'),
        url(r'^/register$', RegisterUserHandler, name='register'),
        url(r'^/login', LoginUserHandler, name='login'),
    ]