# coding=utf-8
# from yuntool.db.handler import DbHandler
from yuntool.db.field import CharField
from yuntool.db.models import Model
from yuntool.chart.sheet import create_sheet
from yuntool.chart.plot import draw_curve, draw_bar
from yuntool.email.smtp import send_mail

DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'test',
    'charset': 'utf8mb4'
}


class TestOrm(Model):
    # 你可能有多个字段，但是你不用全都定义在这，在这定义的字段都是你要展示的字段
    # 不在这定义字段并不影响下边的筛选，当然你只能筛选数据表中存在的字段
    title = CharField()
    label = CharField()

    class meta:
        db_config = DB_CONFIG
        db_table = 'what_do'


def test_get_orm():
    select_term = {
        'label__une': 2,
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
    # ---------------------
    print('------------------')
    res = TestOrm.objects.filter(label=1, title='test10').data()
    for r in res:
        # only print the fields that are defined in TestOrm
        data.append([r.title, r.label])
        print(r.title)

    title = 'test_sheet'
    hearder_list = ['title', 'label']
    f = create_sheet(title, hearder_list, data)
    new_f = open('text.xlsx', 'wb')
    new_f.write(f.read())
    new_f.close()
    f.close()


def test_create_orm(i):
    create_data = {
        'label': 1,
        'title': 'test_{0}'.format(i)
    }
    # print '---------------{0}-------------------'.format(send_time_gte)
    TestOrm.create(**create_data)


def test_update_orm():
    update_data = {
        'title': 'hello yunsonbai',
        'label': 10
    }
    res = TestOrm.objects.filter(id__in=[1, 2]).data()
    for r in res:
        r.update(**update_data)
    # or
    res = TestOrm.objects.filter(id=3).first().data()
    res.update(**update_data)


def test_delete_orm():
    res = TestOrm.objects.filter(id__in=[7, ]).data()
    for r in res:
        result = r.delete()
        print(result)


def test_curve():
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
    new_f = open('text_curve.png', 'wb')
    new_f.write(picture.read())
    new_f.close()
    picture.seek(0)
    return picture


def test_bar():
    x = [
        ['2016-06-28', '2016-06-29', '2016-06-30',
         '2016-07-01', '2016-07-02', '2016-07-03', '2016-07-04'
         ],
        ['2016-06-28', '2016-06-29', '2016-06-30', '2016-07-01',
         '2016-07-02', '2016-07-03', '2016-07-04']]
    y = [
        [270, 279, 288, 273, 248, 232, 293],
        [2482, 1890, 2359, 7506, 14561, 14741, 16191]]
    picture = draw_bar(
        x, y, xlabel=['date', 'date'], ylabel=['num', 'num1'], merge=True)
    new_f = open('text_merge.png', 'wb')
    new_f.write(picture.read())
    new_f.close()
    picture.seek(0)
    return picture


def test_email(picture):
    # test email
    from_user = 'yunsonbai@sohu.com'
    from_user_passwd = 'xxxxxx'
    mail_server = '192.168.95.xx'
    mail_server_port = 'xx'
    to_users = ['1942893504@qq.com']
    try:
        subject = '关于test'.decode('utf-8')
    except:
        subject = '关于test'
    content = '请回复'
    send_mail(
        from_user, from_user_passwd, to_users,
        subject, content, mail_server,
        mail_server_port=mail_server_port,
        picture=picture.getvalue())
    picture.close()

if __name__ == "__main__":
    # test_get_orm()
    # for i in range(10, 20):
    #     test_create_orm(i)
    # test_update_orm()
    # test_delete_orm()
    picture = test_curve()
    # picture = test_bar()
    # test_email(picture)
