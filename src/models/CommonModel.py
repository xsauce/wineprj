import uuid
import datetime
from peewee import Model, Field, CharField, IntegerField
from peewee import MySQLDatabase
from playhouse.shortcuts import model_to_dict
import settings
from const import VALUE
from const import DISPLAY
from utils.cache import cache

__author__ = 'sam'


def m2d(models):
    '''
    model to dict
    :param models: list or peewee Model
    :return: dict list or dict or None
    '''
    try:
        if models:
            result = model_to_dict(models)
        else:
            result = {}
    except:
        result = [model_to_dict(m) for m in models]
    return result

def _get_db():
    db = settings.CURRENT_DB
    conf = settings.DB_CONFIG[db]
    if conf['type'] == 'mysql':
        db_conf = conf['conf']
        return MySQLDatabase(
            db,
            host=db_conf['host'],
            port=db_conf['port'],
            user=db_conf['user'],
            passwd=db_conf['password'],
            charset='utf8',
            fields={'uuid': 'CHAR(36)', 'timestamp': 'TIMESTAMP'}
        )
    return None


DB = _get_db()


class CacheModel(object):
    __objname__ = ''

    @classmethod
    def get_display(cls, val):
        val = int(val)
        for i in cls.select():
            if i[VALUE] == val:
                return i[DISPLAY]

    @classmethod
    def get_value(cls, dis):
        for i in cls.select():
            if i[DISPLAY] == dis:
                return i[VALUE]

    @classmethod
    def select(cls):
        return cache.get(cls.__objname__)

    @classmethod
    def value_list(cls):
        return [d['value'] for d in cls.select()]

    @classmethod
    def choices(cls):
        return [(i[VALUE], i[DISPLAY]) for i in cls.select()]


class BaseModel(Model):
    class Meta:
        database = DB

# custom field
class UUIDField(Field):
    db_field = 'uuid'

    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return str(value)


class TimeStampField(Field):
    db_field = 'timestamp'

    def db_value(self, value):
        return str(value)

    def python_value(self, value):
        return value

class SessionDB(BaseModel):
    session_id = UUIDField(primary_key=True)
    sval = CharField(null=False, max_length=1000)
    expiry_time = IntegerField(null=False)

# class CommonModel(object):
#     __tablename__ = ''
#     __pk__ = ''
#     __insert_method__ = INSERT_DEFAULT
#     to_sql_param = MySQLParameterize.to_sql_param
#     to_sql_param_list = MySQLParameterize.to_sql_param_list
#
#     def __init__(self, fields=None):
#         if not (fields is None):
#             for k, v in fields.items():
#                 if k in self.all_field():
#                     setattr(self, k, v)
#
#     @classmethod
#     def choice_digitalize(cls, choice, choice_list_name):
#         cache_attr = '__%s_CHOICE_DIGITAL_KV__' % choice_list_name
#         if hasattr(cls, cache_attr):
#             return getattr(cls, cache_attr)[choice]
#         else:
#             choice_attr = getattr(cls, choice_list_name)
#             cache_dict = {}
#             for k, v in choice_attr:
#                 cache_dict[k] = v
#             return cache_dict[choice]
#
#     @classmethod
#     def choice_display(cls, num, choice_list_name):
#         cache_attr = '__%s_DIGITAL_CHOICE_KV__' % choice_list_name
#         if hasattr(cls, cache_attr):
#             return getattr(cls, cache_attr)[num]
#         else:
#             choice_attr = getattr(cls, choice_list_name)
#             cache_dict = {}
#             for v, k in choice_attr:
#                 cache_dict[v] = k
#             return cache_dict[num]
#
#
#     @classmethod
#     def dbrow_to_obj(cls, dbrow, mapping=None):
#         if not dbrow:
#             return None
#         dic = None
#         if not isinstance(dbrow, dict):
#             for i in range(len(dbrow)):
#                 dic[mapping[i]] = dbrow[i]
#         else:
#             dic = dbrow
#         obj = cls()
#         for k, v in dic.items():
#             setattr(obj, k, v)
#         return obj
#
#     @classmethod
#     def all_field(cls):
#         obj_dict = cls.__dict__
#         return filter(lambda x: type(obj_dict[x]) == type(None) and not x.startswith('__'), obj_dict)
#
#     @classmethod
#     def find(cls, select_fields='', sql_value=None, where_str='', return_obj=True):
#         select_fields = select_fields if select_fields else cls.all_field()
#         where_str = 'where %s' % where_str if where_str else ''
#         sql = 'select %s from %s %s' % (','.join(select_fields), cls.__tablename__, where_str)
#         result = SqlHelper().query(sql, sql_value)
#         if return_obj:
#             return [cls.dbrow_to_obj(x) for x in result]
#         else:
#             return result
#
#     @classmethod
#     def find_one(cls, select_fields='', sql_value=None, where_str='', return_obj=True):
#         select_fields = select_fields if select_fields else cls.all_field()
#         where_str = 'where %s' % where_str if where_str else ''
#         sql = 'select %s from %s %s' % (','.join(select_fields), cls.__tablename__, where_str)
#         result = SqlHelper().query_one(sql, sql_value)
#         if return_obj:
#             return cls.dbrow_to_obj(result)
#         else:
#             return result
#
#     @classmethod
#     def insert_many_with_autoincr(cls, insert_obj):
#         insert_values = vars(insert_obj)
#         insert_values.pop(cls.__pk__)
#         insert_fields = insert_values.keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute_many(sql, insert_values)
#
#     @classmethod
#     def insert_one_with_autoincr_return_pk(cls, insert_obj):
#         insert_values = vars(insert_obj)
#         insert_values.pop(cls.__pk__)
#         insert_fields = insert_values.keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s) values(%s);SELECT @@IDENTITY;' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute(sql, insert_values)
#         return insert_values[cls.__pk__]
#
#     @classmethod
#     def insert_one_with_return_pk(cls, insert_obj):
#         insert_values = vars(insert_obj)
#         insert_values[cls.__pk__] = str(uuid.uuid4())
#         insert_fields = insert_values.keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute(sql, insert_values)
#         return insert_values[cls.__pk__]
#
#     @classmethod
#     def insert_many_with_return_pk(cls, insert_obj_list):
#         pk_list = []
#         insert_values = []
#         for obj in insert_obj_list:
#             iv = vars(obj)
#             iv[cls.__pk__] = (uuid.uuid4())
#             pk_list.append(iv[cls.__pk__])
#             insert_values.append(iv)
#         insert_fields = insert_values[0].keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute_many(sql, insert_values)
#         return pk_list
#
#     @classmethod
#     def insert_one_with_created_updated_at_return_pk(cls, insert_obj):
#         insert_values = vars(insert_obj)
#         insert_values[cls.__pk__] = str(uuid.uuid4())
#         insert_fields = insert_values.keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute(sql, insert_values)
#         return insert_values[cls.__pk__]
#
#     @classmethod
#     def insert_many_with_created_updated_at_return_pk(cls, insert_obj_list):
#         if not isinstance(insert_obj_list, list):
#             raise Exception('insert values is not list type')
#         pk_list = []
#         insert_values = []
#         for obj in insert_obj_list:
#             iv = vars(obj)
#             iv[cls.__pk__] = (uuid.uuid4())
#             pk_list.append(iv[cls.__pk__])
#             insert_values.append(iv)
#         insert_fields = insert_values[0].keys()
#         insert_params = cls.to_sql_param_list(insert_fields)
#         sql = 'insert into %s(%s,created_at, updated_at) values(%s,NOW(),NOW())' % (cls.__tablename__, ','.join(insert_fields), ','.join(insert_params))
#         SqlHelper().execute_many(sql, insert_values)
#         return pk_list
#
#     @classmethod
#     def insert_one(cls, insert_obj, insert_method=None):
#         im = cls.__insert_method__ if insert_method is None else insert_method
#         if im == INSERT_DEFAULT:
#             insert_value = vars(insert_obj)
#             insert_fields = insert_value.keys()
#             sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(cls.to_sql_param_list(insert_fields)))
#             return SqlHelper().execute(sql, insert_value)
#         elif im == RTN_PK:
#             return cls.insert_one_with_return_pk(insert_obj)
#         elif im == DATE_DEFAULT_RTN_PK:
#             return cls.insert_one_with_created_updated_at_return_pk(insert_obj)
#         elif im == AUTOINCR_RTN_PK:
#             return cls.insert_one_with_autoincr_return_pk(insert_obj)
#
#     @classmethod
#     def insert_many(cls, insert_obj_list, insert_method=None):
#         im = cls.__insert_method__ if insert_method is None else insert_method
#         if im == INSERT_DEFAULT:
#             insert_values = []
#             for obj in insert_obj_list:
#                 insert_values.append(vars(obj))
#             insert_fields = insert_values[0].keys()
#             sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(cls.to_sql_param_list(insert_fields)))
#             return SqlHelper().execute_many(sql, insert_values)
#         elif im == RTN_PK:
#             return cls.insert_many_with_return_pk(insert_obj_list)
#         elif im == DATE_DEFAULT_RTN_PK:
#             return cls.insert_many_with_created_updated_at_return_pk(insert_obj_list)
#         elif im == AUTOINCR_RTN_PK:
#             return cls.insert_many_with_autoincr(insert_obj_list)
#
#     @classmethod
#     def update(cls, update_value, update_fields, where_str):
#         update_fields_str = ','.join(cls.to_sql_param_list(update_fields))
#         where_str = 'where ' + where_str if where_str else ''
#         sql = 'update %s set %s %s' % (cls.__tablename__, update_fields_str, where_str)
#         return SqlHelper().execute(sql, update_value)
#
#     @classmethod
#     def update_many(cls, update_values, update_fields, where_str):
#         update_fields_str = ','.join(cls.to_sql_param_list(update_fields))
#         where_str = 'where ' + where_str if where_str else ''
#         sql = 'update %s set %s %s' % (cls.__tablename__, update_fields_str, where_str)
#         return SqlHelper().execute_many(sql, update_values)
#
#     @classmethod
#     def delete(cls, delete_value, where_str=''):
#         where_str = 'where ' + where_str if where_str else ''
#         sql = 'delete from %s %s' % (cls.__tablename__, where_str)
#         return SqlHelper().execute(sql, delete_value)
#
#     @classmethod
#     def delete_many(cls, delete_values, where_str=''):
#         where_str = 'where ' + where_str if where_str else ''
#         sql = 'delete from %s %s' % (cls.__tablename__, where_str)
#         return SqlHelper().execute_many(sql, delete_values)
