from models.wineshop import Product, ShipCity, Poster
from readonly_cache_data import PAY_SORTS, RECEIPT_CONTENT
from utils.sqlhelper import WHERE_CONDITION


class ProductLL(object):
    @classmethod
    def img_url_str_to_array(cls, r):
        r['img_url'] = r.get('img_url', '').split(',')
    @classmethod
    def query_product_list(cls, query_condition):
        where_str, where_values = '', {}
        if query_condition:
            where_str, where_values = WHERE_CONDITION.build(query_condition)
        product_list = Product.find(where_str=where_str, sql_value=where_values)
        for p in product_list:
            cls.img_url_str_to_array(p)
        return product_list

    @classmethod
    def get_product_by_pid_list(cls, pid_list):
        where_value, where_str = WHERE_CONDITION.IN('pid', pid_list)
        product_list = Product.find(where_str=where_str, sql_value=where_value, return_obj=False)
        for p in product_list:
            cls.img_url_str_to_array(p)
        return product_list

    @classmethod
    def get_grape_sort_list(cls):
        result = Product.find(select_fields=['distinct grape_sort'])
        grape_sort_list = []
        for d in result:
            grape_sort_list.append(d['grape_sort'])
        return grape_sort_list

    @classmethod
    def get_one_by_pid(cls, pid):
        where_value, where_str = WHERE_CONDITION.EXACT('pid', pid)
        rs = Product.find_one(where_str=where_str, sql_value=where_value)
        if rs:
            cls.img_url_str_to_array(rs)
        else:
            rs = {}
        return rs


class ShipCityLL(object):
    @classmethod
    def district_to_array(cls, row):
        row['district'] = row.get('district', '').decode('utf-8').split(',')

    @classmethod
    def get_all_ship_cities(cls):
        rs = ShipCity.find(select_fields=['name', 'district'])
        if rs:
            ds = {}
            for r in rs:
                cls.district_to_array(r)
                ds[r['name'].decode('utf-8')] = r['district']
            return ds
        else:
            return {}


class PosterLL(object):
    @classmethod
    def get_home_posts(cls, place):
        result = Poster.find_by_place(place)
        return result if result else []

class PaySortLL(object):
    @classmethod
    def get_all_sort(cls):
        return PAY_SORTS

class ReceiptLL(object):
    @classmethod
    def get_all_content(cls):
        return RECEIPT_CONTENT

