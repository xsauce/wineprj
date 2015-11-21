# coding:utf-8
import argparse
import sys
from utils.image_tool import batch_create_thumbnail, batch_normalized_photo
from utils.mongohelper import MongoHelper

__author__ = 'sam'
from tornado.ioloop import IOLoop
from wsgi import webapp


class WebManager(object):
    def __init__(self):
        pass

    def start_webapp(self, port):
        app = webapp()
        app.listen(port)
        IOLoop.current().start()

    def product_thumbnail(self):
        batch_create_thumbnail([(500, 500), (100, 100)])

    def init_test_db(self):
        db = MongoHelper().connect()
        # import random
        # desc_word = [u'好喝', u'高大上', u'一分价钱一分货', u'酸就是瑟', u'有品位', u'口感适中']
        # attachment = []
        # for i in range(10):
        #     attachment.append(
        #         {'aid': uuid.uuid4(),
        #          'name': [u'起瓶盖', u'酒塞'][random.randint(0, 1)],
        #          'store_count': random.randint(0, 100),
        #          'sale_count': random.randint(0, 100),
        #          'description': [u'好用', u'精致'][random.randint(0, 1)]
        #          })
        #
        # attachment_collection = db['attachment']
        # attachment_collection.remove()
        # results = attachment_collection.insert_many(attachment)
        # print 'attachment insert 10 record'
        # products = []
        # imgs = ['photo/' + str(i) + '.jpg' for i in range(10)]
        # for i in range(100):
        #     products.append(
        #         {
        #             'name': 'wine' + str(i),
        #             'description': desc_word[random.randint(0, 4)] + ',' + desc_word[random.randint(0, 4)],
        #             'comment_count': random.randint(0, 99),
        #             'store_count': random.randint(0, 99),
        #             'sale_count': random.randint(0, 99),
        #             'volume': random.randint(375, 999),
        #             'img': [
        #                 {'uri': imgs[random.randint(0, 9)], 'seq': 1},
        #                 {'uri': imgs[random.randint(0, 9)], 'seq': 2}
        #             ],
        #             'attachment': (results.inserted_ids[random.randint(0, 9)], results.inserted_ids[random.randint(0, 9)]),
        #             'price': random.randint(50, 200),
        #             'brand': [u'拉菲', u'博若莱', u'圣保罗', u'浪迪', u'大宝'][random.randint(0, 4)],
        #             'country': [u'中国', u'法国',u'利亚', u'意大利', u'美国'][random.randint(0, 4)],
        #             'area': [u'波尔多', u'西安', u'东南奥', u'勃艮第', u'奥克'][random.randint(0, 4)],
        #             'grape_sort': [u'美乐', u'赤霞珠', u'西拉', u'长相思', u'马卡贝奥'][random.randint(0, 4)],
        #             'scene': [u'泡妞', u'商务', u'聚会', u'节日拜访'][random.randint(0, 3)],
        #             'level': [u'AOC', u'VDQS', u'VCE', u'DO'][random.randint(0, 3)],
        #             'sort': [u'红葡萄酒', u'白葡萄酒', u'起泡酒', u'桃红葡萄酒'][random.randint(0, 3)]
        #         }
        #     )
        # product_collection = db['product']
        # product_collection.remove()
        # product_collection.insert_many(products)
        # print 'product insert 100 record'
        # ship_city = db['ship_city']
        # ship_city.remove()
        # ship_city.insert_many([
        #     {'name': u'上海市', 'district': [
        #         {'name': u'闵行区'},
        #         {'name': u'静安区'},
        #         {'name': u'徐汇区'},
        #         {'name': u'黄浦区'}
        #     ]},
        #     {'name': u'江苏省', 'district': [
        #         {'name': u'南通市'},
        #         {'name': u'南京市'},
        #         {'name': u'苏州市'},
        #         {'name': u'常州市'}
        #     ]}
        # ])
        # print 'ship city insert 2'

        # posters = db['poster']
        # posters.remove()
        # batch_normalized_photo([(1024, 512)], filter_name=r'post\d')
        # posters.insert_many([
        #     {'uri': 'photo/post1.jpg', 'description': u'海报1', 'show_place':'home', 'seq': 1},
        #     {'uri': 'photo/post2.jpg', 'description': u'海报2', 'show_place':'home', 'seq': 2},
        #     {'uri': 'photo/post3.jpg', 'description': u'海报3', 'show_place':'home', 'seq': 3}
        # ])
        # print 'poster insert 3'

        pay_sort = db['pay_sort']
        pay_sort.remove()
        pay_sort.insert_many([{'name': u'支付宝'}, {'name': u'货到付款'}])

        print 'pay_sort insert 2'

        print 'finish'


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='wine prj args help')
    parser.add_argument('-startwebapp', help='start web app', default=0, type=int, metavar='port')
    parser.add_argument('-testdb', help='init test db', action='store_true')
    parser.add_argument('-product_thumbnail', action='store_true')
    args = parser.parse_args(sys.argv[1:])
    manager = WebManager()
    if args.testdb:
        manager.init_test_db()
        exit(0)
    if args.product_thumbnail:
        manager.product_thumbnail()
        exit(0)
    if args.startwebapp:
        print 'web application is running...'
        manager.start_webapp(args.startwebapp)
        exit(0)



