# coding=utf-8
from yuntool.db.handler import DbHandler
from yuntool.db.field import CharField
from yuntool.db.models import Model
from yuntool.chart.sheet import create_sheet
from yuntool.chart.plot import draw_curve

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'whatdo',
    'charset': 'utf8mb4'
}


class TestOrm(Model):
    db_table = 'what_do'
    title = CharField()
    label = CharField()


def test():
    DbHandler.connect(**db_config)
    select_term = {
        'type__une': 2,
        # 'type__eq': 100,
        # 'send_time__gte': '2015-09-25 00:00:00',
        # 'send_time__gte': send_time_gte + ' 00:00:00',
        # 'send_time__lte': send_time_gte + ' 23:59:59'
    }
    # print '---------------{0}-------------------'.format(send_time_gte)
    queryset = TestOrm.objects.filter(**select_term)
    count = queryset.count()
    res = queryset.data()
    print(count)
    data = []
    for r in res:
        # only print the fields that are defined in TestOrm
        data.append([r.title, r.label])
        print(r.title)
    print('----------------------')
    res_limit = queryset.limit(1, 2).data()
    for r in res_limit:
        # only print the fields that are defined in TestOrm
        print(r.title)

    title = 'test_sheet'
    hearder_list = ['title', 'label']
    f = create_sheet(title, hearder_list, data)
    new_f = open('text.xlsx', 'wb')
    new_f.write(f.read())
    new_f.close()
    f.close()
    # test curve
    x = [
        ['2016-06-28', '2016-06-29', '2016-06-30',
         '2016-07-01', '2016-07-02', '2016-07-03', '2016-07-04'
         ],
        ['2016-06-28', '2016-06-29', '2016-06-30', '2016-07-01',
         '2016-07-02', '2016-07-03', '2016-07-04']]
    y = [
        [270, 279, 288, 273, 248, 232, 293],
        [2482, 1890, 2359, 7506, 14561, 14741, 16191]]
    picture = draw_curve(
        x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'])
    new_f = open('text.jpg', 'wb')
    new_f.write(picture.read())
    new_f.close()
    picture.close()

if __name__ == "__main__":
    test()
