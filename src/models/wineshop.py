import uuid

__author__ = 'sam'
from CommonModel import *


class ShipCity(CommonModel):
    __tablename__ = 'ship_city'
    city_id = None
    name = None
    district = None

    @classmethod
    def to_obj(cls, row):
        c = ShipCity()
        c.name = row[0]
        c.district = row[1].split(',')
        return c

    @classmethod
    def find_all_cities(cls):
        sql = 'select name, district from %s' % cls.__tablename__
        rs = SqlHelper(return_dict=True).query(sql, None)
        cities = [cls.to_obj(row) for row in rs]
        return cities

    @classmethod
    def find_one_city(cls, city_name):
        sql = 'select name, district from %s where name=?name' % cls.__tablename__
        rs = SqlHelper(return_dict=True).query_one(sql, {'name': city_name})
        return cls.to_obj(rs)


class Product(CommonModel):
    __tablename__ = 'product'
    pid = None
    name = None
    img_url = None
    parent_id = None
    description = None
    volume = None
    price = None
    brand = None
    country = None
    area = None
    grape_sort = None
    scene = None
    wine_level = None
    sort = None
    created_at = None
    updated_at = None

    @classmethod
    def insert_one_product(cls, product):
        product.pid = str(uuid.uuid4())
        insert_fields = product.keys()
        insert_params = cls.to_sql_params(insert_fields)
        sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' %(cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
        SqlHelper().execute(sql, product.__dict__)
        return product.pid

    @classmethod
    def insert_many_product(cls, products):
        pid_list = []
        for p in products:
            p['pid'] = str(uuid.uuid4())
            pid_list.append(p['pid'])
        insert_fields = products[0].keys()
        insert_params = cls.to_sql_param_list(insert_fields)
        sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' %(cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
        SqlHelper().execute_many(sql, [p for p in products])
        return pid_list


class Poster(CommonModel):
    __tablename__ = 'poster'
    poster_id = None
    description = None
    show_place = None
    seq = None

    @classmethod
    def find_by_place(cls, place):
        rs = cls.find(select_fields=cls.all_field(), sql_value={'show_place': place}, where_str='show_place=?show_place', return_obj=True)
        return rs








