# coding=utf-8
import MySQLdb


class DbHandler(object):
    autocommit = True
    conn = None

    @classmethod
    def connect(cls, **db_config):
        cls.conn = MySQLdb.connect(host=db_config.get('host', 'localhost'),
                                   port=db_config.get('port', 3306),
                                   user=db_config.get('user', 'root'),
                                   passwd=db_config.get('password', ''),
                                   db=db_config.get('database', 'test'),
                                   charset=db_config.get('charset', 'utf8'))
        cls.conn.autocommit(cls.autocommit)

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
