# coding=utf-8
import MySQLdb


class DbHandler(object):
    autocommit = True
    conn = None

    @classmethod
    def connect(cls, **db_config):
        autocommit = db_config.get("autocommit", True)
        database = db_config.get('database', 'test')
        cls.conn = MySQLdb.connect(host=db_config.get('host', 'localhost'),
                                   port=db_config.get('port', 3306),
                                   user=db_config.get('user', 'root'),
                                   passwd=db_config.get('password', ''),
                                   db=database,
                                   charset=db_config.get('charset', 'utf8'),
                                   autocommit=autocommit
                                   )
        cls.conn.select_db(database)

    @classmethod
    def get_conn(cls):
        if not cls.conn or not cls.conn.open:
            cls.connect()
        try:
            cls.conn.ping()
        except MySQLdb.OperationalError:
            cls.connect()
        return cls.conn

    @classmethod
    def execute(cls, *args):
        cursor = cls.get_conn().cursor()
        cursor.execute(*args)
        return cursor

    def __del__(self):
        if self.conn and self.conn.open:
            self.conn.close()
