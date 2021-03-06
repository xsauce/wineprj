import MySQLdb
import settings

class MySQLParameterize:
    @classmethod
    def to_sql_param(cls, field):
        return '%(' + field + ')s'

    @classmethod
    def to_sql_param_list(cls, fields):
        return ['%(' + x + ')s' for x in fields]


class WHERE_CONDITION:
    @classmethod
    def EXACT(cls, k, v):
        return {k: v}, '%s=%s' % (k, MySQLParameterize.to_sql_param(k))

    @classmethod
    def LIKE(cls, k, v):
        return {k: v}, "%s like %%%s%%" % MySQLParameterize.to_sql_param(k)

    @classmethod
    def IN(cls, k, v):
        d = {}
        for i, iv in enumerate(v):
            d['%s#%s' % (k, i)] = iv
        w_str = '%s in (%s)' % (k, ','.join(MySQLParameterize.to_sql_param_list([k + '#' + str(i) for i in range(len(v))])))
        return d, w_str

    @classmethod
    def RANGE(cls, k, v):
        d = {}
        d['k#min'] = min(v)
        d['k#max'] = max(v)
        return d, 'BETWEEN %s and %s' % (MySQLParameterize.to_sql_param(k + '#min'), MySQLParameterize.to_sql_param(k + '#max'))

    @classmethod
    def build(cls, where_list):
        where_str, where_values = [], {}
        for k, v, sort_func in where_list:
            w_value, w_str = sort_func(k, v)
            where_str.append(w_str)
            where_values.update(w_value)
        return ' and '.join(where_str), where_values

class ConnectionManager(object):
    def __init__(self):
        self.connections = {}
        self._pool = None

    def open(self, db, use_connection_pool=True):
        if db not in self.connections:
            db_conf = settings.DB_CONFIG[db]
            self.connections[db] = self._get_conn(db, db_conf, use_connection_pool)

    def _get_conn(self, db, db_conf, use_connection_pool):
        db_type = db_conf['type']
        conf = db_conf['conf']
        if use_connection_pool:
            if not self._pool:
                if db_type == 'mysql':
                    self._pool = PooledDB(creator=MySQLdb, mincached=1, maxcached=20,
                                          host=conf['host'],
                                          port=conf['port'],
                                          user=conf['user'],
                                          passwd=conf['password'],
                                          db=db,
                                          use_unicode=False,
                                          charset='utf8')
            return self._pool.connection()
        else:
            if db_conf['type'] == 'mysql':
                return MySQLdb.connect(host=conf['host'],
                                       port=conf['port'],
                                       user=conf['user'],
                                       passwd=conf['password'],
                                       db=db, charset='utf8')

    def commit(self, db):
        if db in self.connections:
            self.connections[db].commit()

    def rollback(self, db):
        if db in self.connections:
            self.connections[db].rollback()

    def get_cursor(self, db, dict_cursor):
        if db in self.connections:
            if dict_cursor:
                return self.connections[db].cursor(cursorclass=MySQLdb.cursors.DictCursor)
            else:
                return self.connections[db].cursor()
        return None

    def close(self, db):
        if db in self.connections:
            self.connections[db].close()
            del self.connections[db]


class TransactionContext(object):
    def __init__(self, db=settings.CURRENT_DB):
        self.db = db

    def __enter__(self):
        self.sqlhelper = SqlHelper(self.db)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.sqlhelper.commit()
            return True
        else:
            self.sqlhelper.rollback()
            return False


class SqlHelper(object):
    def __init__(self, db=settings.CURRENT_DB, return_dict=True):
        self.db = db
        _conn_manager.open(db)
        self.cur = _conn_manager.get_cursor(db, return_dict)

    def close(self):
        _conn_manager.close(self.db)

    def rollback(self):
        _conn_manager.rollback(self.db)

    def commit(self):
        _conn_manager.commit(self.db)

    def query(self, sql, sql_values):
        self.cur.execute(sql, sql_values)
        result = self.cur.fetchall()
        if result:
            return result
        else:
            return []

    def query_one(self, sql, sql_values):
        self.cur.execute(sql, sql_values)
        result = self.cur.fetchone()
        if result:
            return result
        else:
            return []

    def execute_many(self, sql, values):
        if not isinstance(values, list):
            raise Exception('parameter values in executemany must be a list')
        return self.cur.executemany(sql, values)

    def execute(self, sql, values):
        return self.cur.execute(sql, values)


_conn_manager = ConnectionManager()
