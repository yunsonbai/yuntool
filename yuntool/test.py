# coding=utf-8
from songdb.models import Database
from songdb import models
import datetime

db_config = {
    'host': '192.168.96.95',
    'port': 3308,
    'user': 'root',
    'password': 'root',
    'database': 'direct_message',
    'charset': 'utf8mb4'
}


class TestOrm(models.Model):
    db_table = 'message'
    msg = models.CharField()
    to_user_id = models.CharField()
    from_user_id = models.CharField()


def get_num(send_time_gte):
    Database.connect(**db_config)
    select_term = {
        'type__une': 100,
        'send_time__gte': '2016-05-01 00:00:00',
        'from_user_id': 'yunsonbai@sohu.com'
        # 'send_time__gte': '2015-09-25 00:00:00',
        # 'send_time__gte': send_time_gte + ' 00:00:00',
        # 'send_time__lte': send_time_gte + ' 23:59:59'
    }
    # print '---------------{0}-------------------'.format(send_time_gte)
    # print 'total_msg_num:', TestOrm.objects.filter(**select_term).count()
    # res = TestOrm.objects.filter(**select_term).order_by('type').limit(1, 2)
    # res = TestOrm.objects.filter(
    #     **select_term).order_by('type').limit(1, 2).data()
    res = TestOrm.objects.filter(
        type=100, send_time__gte='2016-05-01 00:00:00', from_user_id='yunsonbai@sohu.com').data()
    print res
    for r in res:
        print r.from_user_id
    # res = TestOrm.objects.filter(**select_term).all()
    # users = []
    # for r in res:
    #     if r.from_user_id not in users:
    #         users.append(r.from_user_id)
    # print 'user_num:', len(users)


def get_7_message_user():
    for i in xrange(1, 2):
        get_num(
            send_time_gte=str(datetime.date.today() - datetime.timedelta(
                days=i)))

if __name__ == "__main__":
    get_7_message_user()
