__author__ = 'sam'
from utils.sqlhelper import SqlHelper


class CommonModel(object):
    __tablename__ = ''

    def __init__(self, **fields):
        for k, v in fields.items():
            if k in self.all_field():
                setattr(self, k, v)

    @classmethod
    def dbrow_to_obj(cls, dbrow, mapping=None):
        dic = None
        if not isinstance(dbrow, dict):
            for i in range(len(dbrow)):
                dic[mapping[i]] = dbrow[i]
        else:
            dic = dbrow
        obj = cls()
        for k, v in dic.items():
            setattr(obj, k, v)
        return obj
    @classmethod
    def to_sql_param(cls, field):
        return '%(' + field + ')s'

    @classmethod
    def to_sql_param_list(cls, fields):
        return ['%(' + x + ')s' for x in fields]

    @classmethod
    def all_field(cls):
        obj_dict = cls.__dict__
        return filter(lambda x: type(obj_dict[x]) == type(None) and not x.startswith('__'), obj_dict)

    @classmethod
    def find(cls, select_fields='', sql_value=None, where_str='', return_obj=False):
        select_fields = select_fields if select_fields else cls.all_field()
        if where_str:
            sql = 'select %s from %s where %s' % (select_fields, cls.__tablename__, where_str)
        else:
            sql = 'select %s from %s' % (select_fields, cls.__tablename__)
        result = SqlHelper().query(sql, sql_value)
        if return_obj:
            return [cls.dbrow_to_obj(x) for x in result]
        else:
            return result

    @classmethod
    def find_one(cls, select_fields='', sql_value=None, where_str='', return_obj=False):
        select_fields = select_fields if select_fields else cls.all_field()
        if where_str:
            sql = 'select %s from %s where %s' % (select_fields, cls.__tablename__, where_str)
        else:
            sql = 'select %s from %s' % (select_fields, cls.__tablename__)
        result = SqlHelper().query_one(sql, sql_value)
        if return_obj:
            return cls.dbrow_to_obj(result, select_fields)

    @classmethod
    def insert(cls, insert_value, insert_fields=None):
        insert_fields = insert_fields if insert_fields else cls.all_field()
        sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(cls.to_sql_param_list(insert_fields)))
        return SqlHelper().execute(sql, insert_value)

    @classmethod
    def insert_many(cls, insert_values, insert_fields=None):
        insert_fields = insert_fields if insert_fields else cls.all_field()
        sql = 'insert into %s(%s) values(%s)' % (cls.__tablename__, ','.join(insert_fields), ','.join(cls.to_sql_param_list(insert_fields)))
        return SqlHelper().execute_many(sql, insert_values)

    @classmethod
    def update(cls, update_value, update_fields, where_str):
        update_fields_str = ','.join(cls.to_sql_param_list(update_fields))
        where_str = 'where ' + where_str if where_str else ''
        sql = 'update %s set %s %s' % (cls.__tablename__, update_fields_str, where_str)
        return SqlHelper().execute(sql, update_value)

    @classmethod
    def update_many(cls, update_values, update_fields, where_str):
        update_fields_str = ','.join(cls.to_sql_param_list(update_fields))
        where_str = 'where ' + where_str if where_str else ''
        sql = 'update %s set %s %s' % (cls.__tablename__, update_fields_str, where_str)
        return SqlHelper().execute_many(sql, update_values)

    @classmethod
    def delete(cls, delete_value, where_str=''):
        where_str = 'where ' + where_str if where_str else ''
        sql = 'delete from %s %s' % (cls.__tablename__, where_str)
        return SqlHelper().execute(sql, delete_value)

    @classmethod
    def delete_many(cls, delete_values, where_str=''):
        where_str = 'where ' + where_str if where_str else ''
        sql = 'delete from %s %s' % (cls.__tablename__, where_str)
        return SqlHelper().execute_many(sql, delete_values)

