# yuntool
``` bash
    在运营统计上可以帮助你很快出结果
    主要功能:
        1. 采用orm方式操作数据库，方便你日常的数据统计开发
        2. 支持画曲线图和制表
        3. 支持邮件发送(即将添加)
```

# introduce
### support
``` bash
    python2.7/3.5
```

### requirements
``` bash
    six==1.10.0
    openpyxl==2.3.5
    matplotlib==1.5.2
    numpy==1.11.1
```
#### note
```bash
    python2.7需要安装: MySQLdb
    python3.5需要安装: mysqlclient==1.3.7
```

# overview
### example
``` bash
    请看example/DataAnalysis.py
```

#### note
``` bash
    目前不支持自动创建表，所以要使用之前确保表已经存在，在model中定义的字段表中已经存在
```

# model
### Field types
``` bash
    Prikey
    CharField
    IntegerField
    DateTimeField
```

### select
#### select option
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

#### select function
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
        每次查询语句(除去count)最后都要调用data才能查询出数据
    example：
        res = TestModel.objects.filter(**select_term).all().data()
        res = TestModel.objects.filter(**select_term).limit(0, 7).data()
        res = TestModel.objects.filter(**select_term).order_by(id).limit(0, 7).data()
```

#### note
``` bash
    支持单条件筛选和多条件筛选，请看例子
    你可以像使用django查询数据库一样去使用，只是要在最后加入data()**
```
