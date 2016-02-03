# coding:utf-8
import argparse
import csv
import os
import sys
import uuid
import datetime
from tornado import locale
from models.CommonModel import DB, SessionDB
from models.wineshop import *
import settings
from utils.image_tool import batch_normalized_photo, batch_create_thumbnail

__author__ = 'sam'
from tornado.ioloop import IOLoop
from wsgi import webapp


class WebManager(object):
    def __init__(self):
        pass

    def shell(self, args):
        import code
        import sys
        sys.path.append('handler/')
        sys.path.append('logiclayer/')
        sys.path.append('utils/')
        sys.path.append('models/')
        sys.path.append('views/')
        code.interact(local={})

    def build_env(self, args):
        if not args.user:
            print 'incorrect user name'
            return
        user = args.user
        log_dir = settings.LOG_CONF['dir']
        if not os.path.exists(log_dir):
            import subprocess
            subprocess.call('sudo mkdir %s && sudo chown %s %s' % (log_dir, user, log_dir), shell=True)

    def start(self, args):
        port = args.port if args.port else 8080
        app = webapp()
        app.listen(port)
        locale.load_translations(settings.LOCALE_DIR)
        IOLoop.current().start()

    def gen_multi_locale_file(self, args):
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

    def photo_normalized(self, args):
        batch_normalized_photo((300, 300), filter_name='shop\d+')
        batch_normalized_photo((300, 300), filter_name=r'\d+')
        batch_create_thumbnail((30, 30), filter_name=r'\d+')
        batch_normalized_photo((1024, 512), filter_name=r'post\d')

    def init_db(self, args):
        with DB.execution_context() as ctx:
            DB.create_tables([
                Shop,
                ShopPhoto,
                User,
                Administrator,
                Product,
                ProductLabelList,
                ProductSceneList,
                ProductPhoto,
                Repertory,
                RepertoryEntry,
                SaleOrder,
                SaleOrderDetail,
                SaleOrderTrace,
                Poster,
                SessionDB
            ])

    def test_data(self, args):
        with DB.execution_context() as ctx:
            import random
            labels = ProductLabel
            brands = Brand
            countries = Country
            regions = Region
            grape_sort = GrapeSort
            scenes = Scene
            wine_levels = WineLevel
            wine_sorts = WineSort

            ProductSceneList.delete().execute()
            ProductPhoto.delete().execute()
            ProductLabelList.delete().execute()
            Product.delete().execute()
            ShopPhoto.delete().execute()
            Shop.delete().execute()
            shop_list = []
            for i in range(5):
                shop = Shop.create(
                    shop_id=str(uuid.uuid4()),
                    shop_name='shop' + str(i),
                    address='address' + str(i),
                    geo='%s,%s' % (random.randint(100, 200), random.randint(100, 200)),
                    description='shop desciption',
                    created_at=datetime.datetime.now()
                )
                for a in range(2):
                    ShopPhoto.create(
                        hash_value=str(random.randint(1, 8)),
                        photo_type='jpg',
                        shop=shop
                    )
                shop_list.append(shop)

            for i in range(100):
                product = Product.create(
                    pid=str(uuid.uuid4()),
                    name='wine' + str(i),
                    description='wine description',
                    volume=random.randint(375, 999),
                    price=random.randint(50, 200),
                    shop=shop_list[random.randint(0, 4)],
                    brand=brands[random.randint(0, 1)][0],
                    country=countries[random.randint(0, 1)][0],
                    region=regions[random.randint(0, 1)][0],
                    grape_sort=grape_sort[random.randint(0, 4)][0],
                    wine_level=wine_levels[random.randint(0, 2)][0],
                    sort=wine_sorts[random.randint(0, 1)][0],
                    created_at=datetime.datetime.now())
                ProductLabelList.create(
                        product=product,
                        label=labels[random.randint(0, 1)][0]
                )
                for a in range(3):
                    ProductPhoto.create(
                        hash_value=str(random.randint(0, 9)),
                        seq_num=a,
                        photo_type='jpg',
                        product=product,
                        created_at=datetime.datetime.now()
                    )
                for b in range(2):
                    ProductSceneList.create(
                        product=product,
                        scene=scenes[random.randint(0, 3)][0]
                    )
            print 'product insert 100 record'
            Poster.delete().execute()
            posters = [
                {'hash_value': '1', 'description': u'post1', 'place': 'home', 'seq': 1, 'pic_type': 'jpg'},
                {'hash_value': '2', 'description': u'post2', 'place': 'home', 'seq': 2, 'pic_type': 'jpg'},
                {'hash_value': '3', 'description': u'post3', 'place': 'home', 'seq': 3, 'pic_type': 'jpg'}
            ]
            Poster.insert_many(posters).execute()
            print 'poster insert 3'
            print 'finish'


if __name__ == '__main__':
    help_text = '''
    - start {-port(8080)} start web app,
    - test_data create test data,
    - build_env -user=Sam, build running env, required os current user name,
    - photo_normalized, normalized photoes in /static/photo folder,
    - shell, start a shell within this project.
    - gen_multi_local_file, use local_seed.csv to generate some local.csv,
    - init_db, create table
    '''
    parser = argparse.ArgumentParser(description='wine prj args help')
    parser.add_argument('-cmd', type=str, required=True, help=help_text)
    parser.add_argument('-port', default=8080, required=False, type=int)
    parser.add_argument('-user', type=str, default='', required=False)
    args = parser.parse_args(sys.argv[1:])
    manager = WebManager()
    if args.cmd:
        if hasattr(manager, args.cmd):
            getattr(manager, args.cmd)(args)
        else:
            print help_text
        exit(0)


