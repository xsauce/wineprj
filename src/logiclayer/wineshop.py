from models.wineshop import Product, ShipCity, Poster


class WHERE_CONDITION:
    @classmethod
    def EXACT(cls, k, v):
        return {k: v}, '%s=?%s' % k

    @classmethod
    def LIKE(cls, k, v):
        return {k: v}, "%s like '%%?%s%%'" % k

    @classmethod
    def IN(cls, k, v):
        d = {}
        for i, iv in enumerate(v):
            d['%s#%s' % (k, i)] = iv
        w_str = '%s in (%s)' % (k, ','.join(['?' + k + '#' + str(i) for i in range(len(v))]))
        return d, w_str

    @classmethod
    def RANGE(cls, k, v):
        d = {}
        d['k#min'] = min(v)
        d['k#max'] = max(v)
        return d, 'BETWEEN ?%s and ?%s' % (k + '#min', k + '#max')

    @classmethod
    def build(cls, where_list):
        where_str, where_values = [], {}
        for k, v, sort_func in where_list:
            w_value, w_str = sort_func(k, v)
            where_str.append(w_str)
            where_values.update(w_value)
        return ' and '.join(where_str), where_values


def query_product_list_from_db(query_condition):
    where_str, where_values= '', {}
    if query_condition:
        where_str, where_values = WHERE_CONDITION.build(query_condition)
    product_list = Product.find(where_str=where_str, sql_value=where_values)
    return product_list

def get_product_with_id_from_db(pid_list):
    product_list = Product.find(where_str='pid in %s' % ','.join(pid_list), return_obj=False)
    return product_list


def get_all_ship_cities_from_db():
    return [c.__dict__ for c in ShipCity.find_all_cities()]


def get_home_posts_from_db(place):
    result = Poster.find_by_place(place)
    return result if result else []

def get_grape_sort_list():
    result = Product.find(select_fields='distinct grape_sort')
    grape_sort_list = []
    for k, v in result.items():
        grape_sort_list.append(v)
    return grape_sort_list


