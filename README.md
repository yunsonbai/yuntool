# songdb
``` bash
    采用orm方式操作数据库，方便你日常的数据统计开发
```

# introduce
## support
``` bash
    python2.7
```

## requirements
``` bash
    MySQLdb
```
# overview
## example
``` bash
    使用例子
    # coding=utf-8
    from songdb.models import Database
    from songdb import models
    import datetime

    db_config = {
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'user',
        'password': '',
        'database': 'test',
        'charset': 'utf8mb4'
    }


    class TestModel(models.Model):
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
        print 'total_num:', TestModel.objects.filter(**select_term).count()
        res = TestModel.objects.filter(**select_term).all().data()
        # res = TestModel.objects.filter(type='name').all().data()
        #res = TestModel.objects.filter(
        #    type=100,
        #    send_time__gte='2016-05-01 00:00:00',
        #    from_user_id='yunsonbai@sohu.com').data()
        users = []
        for r in res:
            if r.from_user_id not in users:
                users.append(r.from_user_id)
        print 'user_num:', len(users)
```

## note
``` bash
    目前不支持自动创建表，所以要使用之前确保表已经存在，在model中定义的字段表中已经存在
```

# model
## Field types
``` bash
    CharField
    IntegerField
    DateTimeField
```

## select
### select option
``` bash
    'lt': '<',
    'gt': '>',
    'une': '!=',
    'lte': '<=',
    'gte': '>=',
    'eq': '='  #可以不用携带,默认是=
    'in': 'in'

    example：
        field__lt = 2
        field__in = ['one', 'two]
        field__in = ('one', 'two)
```

### selecr function
``` bash
    limit
    order_by
    group_by
    desc_order_by
    first
    all
    count

    note:
        limit 要在 group_by/order_by 后边调用；
        每次查询语句最后都要调用data才能查询出数据
    example：
        res = TestModel.objects.filter(**select_term).all().data()
        res = TestModel.objects.filter(**select_term).limit(0, 7).data()
        res = TestModel.objects.filter(**select_term).order_by(id).limit(0, 7).data()
```

### note
``` bash
    支持单条件筛选和多条件筛选，请看例子
    你可以像使用django查询数据库一样去使用，只是要在最后加入data()**
```
