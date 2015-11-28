from models.CommonModel import CommonModel
from models.wineshop import Product, ShipCity, Poster
from readonly_cache_data import PAY_SORTS, RECEIPT_CONTENT


class WHERE_CONDITION:
    @classmethod
    def EXACT(cls, k, v):
        return {k: v}, '%s=?%s' % k

    @classmethod
    def LIKE(cls, k, v):
        return {k: v}, "%s like %%%s%%" % CommonModel.to_sql_param(k)

    @classmethod
    def IN(cls, k, v):
        d = {}
        for i, iv in enumerate(v):
            d['%s#%s' % (k, i)] = iv
        w_str = '%s in (%s)' % (k, ','.join(CommonModel.to_sql_param_list([k + '#' + str(i) for i in range(len(v))])))
        return d, w_str

    @classmethod
    def RANGE(cls, k, v):
        d = {}
        d['k#min'] = min(v)
        d['k#max'] = max(v)
        return d, 'BETWEEN %s and %s' % (CommonModel.to_sql_param(k + '#min'), CommonModel.to_sql_param(k + '#max'))

    @classmethod
    def build(cls, where_list):
        where_str, where_values = [], {}
        for k, v, sort_func in where_list:
            w_value, w_str = sort_func(k, v)
            where_str.append(w_str)
            where_values.update(w_value)
        return ' and '.join(where_str), where_values

class ProductLL(object):

    @classmethod
    def query_product_list(cls, query_condition):
        where_str, where_values = '', {}
        if query_condition:
            where_str, where_values = WHERE_CONDITION.build(query_condition)
        product_list = Product.find(where_str=where_str, sql_value=where_values)
        return product_list

    @classmethod
    def get_product_by_pid_list(cls, pid_list):
        product_list = Product.find(where_str='pid in %s' % ','.join(pid_list), return_obj=False)
        return product_list

    @classmethod
    def get_grape_sort_list(cls):
        result = Product.find(select_fields='distinct grape_sort')
        grape_sort_list = []
        for k, v in result.items():
            grape_sort_list.append(v)
        return grape_sort_list

    @classmethod
    def get_one_by_pid(cls, pid):
        rs = Product.find_one(where_str='pid=?pid', sql_value={'pid': pid})
        return rs


class ShipCityLL(object):
    @classmethod
    def get_all_ship_cities(cls):
        return [c.__dict__ for c in ShipCity.find_all_cities()]


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

