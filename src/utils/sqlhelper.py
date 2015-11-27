import MySQLdb
from DBUtils.PooledDB import PooledDB
import settings

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
            self.connections[db] = None


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
