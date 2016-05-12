only sport python2.7


使用例子

# coding=utf-8
from songdb.models import Database
from songdb import models
import datetime

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'user',
    'password': 'user',
    'database': 'test',
    'charset': 'utf8mb4'
}


class TestOrm(models.Model):
    db_table = 'msg'
    msg = models.CharField()
    to_user = models.CharField()
    from_user = models.CharField()


def get_num(send_time_gte):
    Database.connect(**db_config)
    select_term = {
        'type__une': 'name',
        'send_time__gte': send_time_gte + ' 00:00:00',
        'send_time__lte': send_time_gte + ' 23:59:59'
    }
    print 'total_num:', TestOrm.objects.filter(**select_term).count()
    res = TestOrm.objects.filter(**select_term).all().data()
    # res = TestOrm.objects.filter(type='name').all().data()
    #res = TestOrm.objects.filter(
    #    type=100, send_time__gte='2016-05-01 00:00:00', from_user_id='yunsonbai@sohu.com').data()
    users = []
    for r in res:
        if r.from_user_id not in users:
            users.append(r.from_user_id)
    print 'user_num:', len(users)


支持：
    1）
        'lt': '<',
        'gt': '>',
        'une': '!=',
        'lte': '<=',
        'gte': '>=',
        'eq': '='  #可以不用携带,默认是=
        使用方式：
            field__lt = 2
    2）
        limit 
        order_by
        first
        all
        count


补充：
    支持但条件筛选和多条件筛选，请看例子
    你可以像使用django查询数据库一样去使用，只是要在最后加入data()