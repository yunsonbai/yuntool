# coding=utf-8
from error import *
from field import (
    Prikey, Field)
from handler import DbHandler


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
            for row in DbHandler.execute(sql, self.params).fetchall():
                inst = self.model
                for idx, f in enumerate(row):
                    setattr(inst, self.model.fields.keys()[idx], f)
                yield inst
        except Exception as e:
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
                row = DbHandler.execute(sql, self.params).fetchone()
                inst = self.model
                for idx, f in enumerate(row):
                    setattr(inst, self.model.fields.keys()[idx], f)
                return inst
            else:
                return self._datas(sql)
        except Exception as e:
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
        (row_cnt, ) = DbHandler.execute(sql, self.params).fetchone()
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
        return DbHandler.execute(sql)

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
        result = DbHandler.execute(sql)
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
            result = DbHandler.execute(sql)
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


def execute_raw_sql(sql, params=None):
    return DbHandler.execute(sql, params) if params else DbHandler.execute(sql)
