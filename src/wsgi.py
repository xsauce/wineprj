# coding:utf-8
from settings import APP_SETTINGS

__author__ = 'sam'
from urls import url_routes
from tornado.web import Application


def webapp():
    return Application(url_routes, **APP_SETTINGS)


