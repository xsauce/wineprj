# coding:utf-8
import argparse
import csv
import os
import sys
import uuid
import collections
from tornado import locale
from models.wineshop import Product, ShipCity, Poster
import settings
from utils.image_tool import batch_create_thumbnail, batch_normalized_photo
# from utils.mongohelper import MongoHelper
from utils.sqlhelper import SqlHelper, TransactionContext

__author__ = 'sam'
from tornado.ioloop import IOLoop
from wsgi import webapp


class WebManager(object):
    def __init__(self):
        pass

    def shell(self):
        import code
        import sys
        sys.path.append('handler/')
        sys.path.append('logiclayer/')
        sys.path.append('utils/')
        sys.path.append('models/')
        sys.path.append('views/')
        code.interact(local={})

    def build_envir(self, user):
        import os
        log_dir = settings.LOG_CONF['dir']
        if not os.path.exists(log_dir):
            import subprocess
            subprocess.call('sudo mkdir %s && sudo chown %s %s' % (log_dir, user, log_dir), shell=True)

    def startwebapp(self, port):
        app = webapp()
        app.listen(port)
        locale.load_translations(settings.LOCALE_DIR)
        IOLoop.current().start()

    def gen_multi_locale_file(self):
        locale_seed_file = os.path.join(settings.ROOT_DIR, 'locale_seed.csv')
        locale_list = {}
        with open(locale_seed_file) as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = row['key']
                for k, v in row.items():
                    if k not in ['key', 'plural']:
                        i_locale = locale_list.setdefault(k, {})
                        i_locale[key] = (v,)
        for i_locale, locale_list in locale_list.items():
            locale_file = os.path.join(settings.LOCALE_DIR, i_locale + '.csv')
            with open(locale_file, 'wb') as f:
                writer = csv.writer(f)
                for key, row in locale_list.items():
                    writer.writerow([key, row[0]])


    def product_thumbnail(self):
        batch_create_thumbnail((50, 50))

    def photo_normalized(self):
        batch_normalized_photo((300, 300), filter_name=r'\d+')
        batch_normalized_photo((1024, 512), filter_name=r'post\d')

    def init_test_db(self):
        with TransactionContext(settings.CURRENT_DB):
            import random
            desc_word = [u'好喝', u'高大上', u'一分价钱一分货', u'酸就是瑟', u'有品位', u'口感适中']
            products = []
            imgs = ['photo/' + str(i) + '.jpg' for i in range(10)]
            for i in range(100):
                products.append(
                    {
                        'name': 'wine' + str(i),
                        'description': desc_word[random.randint(0, 4)] + ',' + desc_word[random.randint(0, 4)],
                        'volume': random.randint(375, 999),
                        'img_url': ','.join([imgs[random.randint(0, 9)], imgs[random.randint(0, 9)]]),
                        'price': random.randint(50, 200),
                        'brand': [u'拉菲', u'博若莱', u'圣保罗', u'浪迪', u'大宝'][random.randint(0, 4)],
                        'country': [u'中国', u'法国',u'利亚', u'意大利', u'美国'][random.randint(0, 4)],
                        'area': [u'波尔多', u'西安', u'东南奥', u'勃艮第', u'奥克'][random.randint(0, 4)],
                        'grape_sort': [u'美乐', u'赤霞珠', u'西拉', u'长相思', u'马卡贝奥'][random.randint(0, 4)],
                        'scene': [u'泡妞', u'商务', u'聚会', u'节日拜访'][random.randint(0, 3)],
                        'wine_level': [u'AOC', u'VDQS', u'VCE', u'DO'][random.randint(0, 3)],
                        'sort': [u'红葡萄酒', u'白葡萄酒', u'起泡酒', u'桃红葡萄酒'][random.randint(0, 3)]
                    }
                )
            Product.delete({})
            Product.insert_many_with_created_updated_at_return_pk('pid', products)
            print 'product insert 100 record'
            ShipCity.delete({})
            cities = [
                {'city_id': str(uuid.uuid4()), 'name': u'上海市', 'district': ','.join([u'闵行区', u'静安区', u'徐汇区', u'黄浦区'])},
                {'city_id': str(uuid.uuid4()), 'name': u'江苏省', 'district': ','.join([u'南通市', u'南京市', u'苏州市', u'常州市'])}
            ]
            ShipCity.insert_many(cities)
            print 'ship city insert 2'
            Poster.delete({})
            posters = [
                {'poster_id': 'post1.jpg', 'description': u'海报1', 'show_place':'home', 'seq': 1},
                {'poster_id': 'post2.jpg', 'description': u'海报2', 'show_place':'home', 'seq': 2},
                {'poster_id': 'post3.jpg', 'description': u'海报3', 'show_place':'home', 'seq': 3}
            ]
            Poster.insert_many(posters)
            print 'poster insert 3'
            print 'finish'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wine prj args help')
    parser.add_argument('-startwebapp', help='start web app', default=0, type=int, metavar='port')
    parser.add_argument('-testdb', help='init test db', action='store_true')
    parser.add_argument('-build_envir', help='build running environment,please input your current user name', type=str)
    parser.add_argument('-product_thumbnail', action='store_true')
    parser.add_argument('-photo_normalized', action='store_true')
    parser.add_argument('-shell', action='store_true')
    parser.add_argument('-gen_multi_locale_file', action='store_true')
    args = parser.parse_args(sys.argv[1:])
    manager = WebManager()
    if args.testdb:
        manager.init_test_db()
        exit(0)
    if args.product_thumbnail:
        manager.product_thumbnail()
        exit(0)
    if args.photo_normalized:
        manager.photo_normalized()
        exit(0)
    if args.build_envir:
        manager.build_envir(args.build_envir)
    if args.startwebapp:
        print 'web application is running...'
        manager.startwebapp(args.startwebapp)
        exit(0)
    if args.shell:
        manager.shell()
    if args.gen_multi_locale_file:
        manager.gen_multi_locale_file()



