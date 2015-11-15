import importlib
import os
import sqlite3
import settings


def withpid(db):
    return db + '#@#' + str(os.getpid())


def dbrow_to_obj(dbrow, cls_name, mapping=None):
    try:
        dic = None
        if not isinstance(dbrow, dict):
            for i in range(len(dbrow)):
                dic[mapping[i]] = dbrow[i]
        else:
            dic = dbrow
        acls = None
        for m in _model_modules:
            if hasattr(m, cls_name):
                acls = getattr(m, cls_name)
                break
        if acls is None:
            raise Exception('Not found class in register models, check out in settings')
        return acls(dic)
    except Exception, e:
        raise






class ConnectionManager(object):
    def __init__(self):
        self.connections = {}

    def open(self, db):
        if withpid(db) not in self.connections:
            db_conf = settings.DB_CONFIG[db]
            if db_conf['type'] == 'sqlite3':
                self.connections[withpid(db)] = sqlite3.connect(db_conf['conf']['uri'])
            elif db_conf['type'] == 'mongodb':
                pass
            elif db_conf['type'] == 'mysql':
                pass

    def commit(self, db):
        if withpid(db) in self.connections:
            self.connections[withpid(db)].commit()

    def rollback(self, db):
        if withpid(db) in self.connections:
            self.connections[withpid(db)].rollback()

    def get_cursor(self, db):
        if withpid(db) in self.connections:
            return self.connections[withpid(db)].cursor()
        return None

    def close(self, db):
        if withpid(db) in self.connections:
            self.connections[withpid(db)].close()
            self.connections[withpid(db)] = None

# def execute_sql(func):
#     def wrapper(*args, **kwargs):
#         conn_manager = Connection()
#         try:
#             conn_manager.open()
#             cur = conn_manager.cursor()
#             result = func(cur, *args, **kwargs)
#             conn_manager.commit()
#             return result
#         except:
#             raise
#         finally:
#             conn_manager.close()
#
#     return wrapper

class SqlHelper(object):
    def __init__(self, db=settings.CURRENT_DB):
        self.db = db
        _conn_manager.open(db)
        self.cur = _conn_manager.get_cursor(db)

    def close(self):
        _conn_manager.close(self.db)

    def rollback(self):
        _conn_manager.rollback(self.db)

    def commit(self):
        _conn_manager.commit(self.db)

    def query_all(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return []

    def query_one(self, sql):
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            return result
        else:
            return []

    def insert(self, table, insert_objs, insert_fields=[], is_batch=False):
        insert_fields = insert_fields if insert_fields else insert_objs[0].all_field()
        insert_fields_str = ','.join(insert_fields)
        sql = 'insert into %s(%s) values(%s)' % (table, insert_fields_str, ','.join([':' + f for f in insert_fields]))
        if is_batch:
            return self.cur.executemany(sql, insert_objs)
        else:
            return self.cur.execute(sql, insert_objs[0])


    def update(self, table, update_objs, where_str, update_fields=[], is_batch=False):
        update_fields = update_fields if update_fields else update_objs[0].all_field()
        update_fields_str = ','.join([f + ':' + f for f in update_fields])
        where_str = 'and ' + where_str if where_str else ''
        sql = 'update %s set %s where 1=1 %s' % (table, update_fields_str, where_str)
        if is_batch:
            return self.cur.executemany(sql, update_objs)
        else:
            return self.cur.execute(sql, update_objs[0])

    def delete(self, table, delete_objs, where_str, is_batch=False):
        where_str = 'and ' + where_str if where_str else ''
        sql = 'delete from %s where 1=1 %s' % (table, where_str)
        if is_batch:
            return self.cur.executemany(sql, delete_objs)
        else:
            return self.cur.execute(sql, delete_objs[0])

_conn_manager = ConnectionManager()
_model_modules = [importlib.import_module(loc) for loc in settings.MODEL_MODULES]

