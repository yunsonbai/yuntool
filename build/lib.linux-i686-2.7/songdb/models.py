# coding=utf-8

import MySQLdb
from error import *
import datetime


class Prikey(object):
    pass


class Field(object):

    def __init__(self, *args, **kwargs):
        for key, val in kwargs.iteritems():
            if val:
                val = str(val).replace('"', '\'')
            setattr(self, key, val)


class CharField(Field):

    def __init__(self, default=None):
        Field.__init__(self, default=default, field_type='CharField')
        pass


class IntegerField(Field):

    def __init__(self, default=None):
        # msyql既然支持int转换,就用一下吧
        default = str(default)
        Field.__init__(self, default=default, field_type='IntegerField')
        pass


class DateTimeField(Field):

    def __init__(self, default=None, auto_now_add=False):
        if auto_now_add:
            default = str(datetime.datetime.now())
        Field.__init__(self, default=default, field_type='DateTimeField')
        pass


class SqlExpr(object):

    operator = {
        'lt': '<',
        'gt': '>',
        'une': '!=',
        'lte': '<=',
        'gte': '>=',
        'eq': '=',
        'in': ' in ',
    }

    def __init__(self, model, kwargs):
        self.first_line = False
        self.model = model
        self.params = kwargs.values()
        equations = []
        i = 0
        for key in kwargs.keys():
            key_spl = key.split('__')
            try:
                equations.append(
                    key_spl[-2] + self.operator[key_spl[-1]] + '%s')
            except:
                equations.append(key_spl[-1] + '=%s')
            i += 1
        self.where_expr = 'where ' + ' and '.join(
            equations) if len(equations) > 0 else ''

    def _make_sql(self):
        if self.model.fields.keys():
            sql = 'select {0} from {1} {2};'.format(
                ', '.join(self.model.fields.keys()),
                self.model.db_table, self.where_expr)
        else:
            sql = 'select * from {0} {1};'.format(
                self.model.db_table, self.where_expr)
        return sql

    def _datas(self, sql):
        try:
            for row in Database.execute(sql, self.params).fetchall():
                inst = self.model
                for idx, f in enumerate(row):
                    setattr(inst, self.model.fields.keys()[idx], f)
                yield inst
        except Exception, e:
            raise e

    def order_by(self, *rows):
        self.where_expr += ' order by {0}'.format('{0}'.format(','.join(rows)))
        return self

    def desc_order_by(self, *rows):
        self.where_expr += ' order by {0} desc'.format(
            '{0}'.format(','.join(rows)))
        return self

    def group_by(self, *rows):
        self.where_expr += ' group by {0}'.format('{0}'.format(','.join(rows)))
        return self

    def limit(self, *rows):
        '''
        function:
            limit the result number
        parameter:
            *rows:
                1
                1, 2
        return:
            object SqlExpr

        '''
        if len(rows) == 1:
            self.where_expr = self.where_expr + ' limit {0}'.format(rows)
        elif len(rows) == 2:
            self.where_expr = self.where_expr + \
                ' limit {0},{1}'.format(rows[0], rows[1])
        return self

    def first(self):
        '''
        function:
            get the first result
        return:
            object SqlExpr
        '''
        self.first_line = True
        return self

    def all(self, sql=None):
        '''
        function:
            get the all result
        return:
            object SqlExpr
        '''
        return self

    def data(self):
        '''
        function:
            get the result
        return:
            if one result:
                return orm
            if more result:
                return generator
        '''
        sql = self._make_sql()
        try:
            if self.first_line:
                row = Database.execute(sql, self.params).fetchone()
                inst = self.model
                for idx, f in enumerate(row):
                    setattr(inst, self.model.fields.keys()[idx], f)
                return inst
            else:
                return self._datas(sql)
        except Exception, e:
            raise e

    def count(self):
        '''
        function:
            get the result num
        return:
            int num
        '''
        sql = 'select count(*) from {0} {1};'.format(self.model.db_table,
                                                     self.where_expr)
        (row_cnt, ) = Database.execute(sql, self.params).fetchone()
        return row_cnt


class MetaModel(type):
    db_table = None
    fields = {}

    def __init__(cls, name, bases, attrs):
        super(MetaModel, cls).__init__(name, bases, attrs)
        fields = {}
        pri_field = 'id'
        fields['id'] = Prikey()
        for key, val in cls.__dict__.iteritems():
            if isinstance(val, Prikey):
                fields.pop(pri_field)
                fields[key] = val
                pri_field = key

            elif isinstance(val, Field):
                fields[key] = val
            else:
                pass
        cls.fields = fields
        cls.pri_field = pri_field
        cls.attrs = attrs
        cls.objects = cls()


class Model(object):
    __metaclass__ = MetaModel

    def update(self, **kwargs):
        '''
        function:
            update data
        params:
            dict
        '''
        for key, val in kwargs.iteritems():
            if val is None or key not in self.fields:
                raise Exception(NORIGHTERROR.format(key))
        where = 'where {0} = {1}'.format(
            self.pri_field, self.__dict__[self.pri_field])
        sql = 'update {0} set {1} {2};'.format(self.db_table, ','.join(
            [key + ' = "{0}"'.format(str(
                kwargs[key]).replace('"', '\'')) for key in kwargs.keys()]),
            where)
        return Database.execute(sql)

    @classmethod
    def create(self, **kwargs):
        '''
        function:
            create one or more data
        params:
            dict
        '''
        for key, val in kwargs.iteritems():
            if val is None or key not in self.fields:
                raise Exception(NORIGHTERROR.format(key))
        for key, val in self.fields.iteritems():
            if isinstance(val, Field):
                if key not in kwargs:
                    if val.default:
                        kwargs[key] = val.default
                    else:
                        raise Exception(FEILDNULLRROR.format(key))
        sql = 'insert ignore into {0}({1}) values ("{2}");'.format(
            self.db_table, ', '.join(kwargs.keys()),
            '","'.join([
                str(kwargs[key]).replace('"', '\'') for key in kwargs.keys()]))
        result = Database.execute(sql)
        if not result._info:
            setattr(result, 'success', True)
        return result

    def delete(self, **kwargs):
        if kwargs:
            datas = self.filter(**kwargs).all()
            where = 'where {0} = {1}'.format(self.pri_field, ' or '.join(
                [str(data.__dict__[self.pri_field]) for data in datas]))
            sql = 'delete from {0} {1};'.format(self.db_table, where)
        else:
            sql = 'delete from {0} where {1} = {2};'.format(
                self.db_table, self.pri_field, self.activity_id)
        try:
            result = Database.execute(sql)
            if not result._info:
                setattr(result, 'success', True)
        except:
            result = object()
            setattr(result, 'success', True)
        return result

    def filter(self, **kwargs):
        '''
        function:
            add filter conditions
        '''
        return SqlExpr(self, kwargs)


class Database(object):
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


def execute_raw_sql(sql, params=None):
    return Database.execute(sql, params) if params else Database.execute(sql)
