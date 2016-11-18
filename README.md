# yuntool
## Overview
* 应用：运营数据统计；快熟查询数据库异常数据；快速数据进行增删改查
* 版本：0.4
* 安装：
	* git clone git@github.com:yunsonbai/yuntool.git
	* python setup.py install
* 主要功能和特点:
	* 采用orm方式操作数据库
    * 支持画图
    	* 曲线图
        * 柱形图
    * 制表excel
    * 支持邮件发送
    	* 纯文字
        * 图加文字

## Requirements
* 开发语言
	* python2.7
	* python3.5
* 依赖库
	* python2.7/3.5
    * six==1.10.0
    * openpyxl==2.3.5
    * matplotlib==1.5.2
    * numpy==1.11.1
    * smtplib

    ##### Note
    ```bash
        python2.7需要安装: MySQLdb
        python3.5需要安装: mysqlclient==1.3.7
    ```

## Quick Start
 [Test Script](https://github.com/yunsonbai/yuntool/tree/master/example)

#### note
``` python
    目前不支持自动创建表，所以要使用之前确保表已经存在，在model中定义的字段表中已经存在
```

## Documentation
* model
	* Field
    	* Prikey
    	* CharField
    	* IntegerField
    	* DateTimeField

	* Filter Data
		* operator
    		* lt: '<'
    		* gt: '>'
    		* une: '!='
    		* lte: '<='
    		* gte: '>='
    		* eq: '=' (可以不用携带,默认是=)
    		* in: 'in'

        ###### Note
        ```python
            1. operator
                field__lt = 2
                field__in = ['one', 'two]
                field__in = ('one', 'two)
            2. filter
                支持单条件或多条件筛选:
                select_term = {
                    'type__une': 2,
                    'send_time__gte': '2015-09-25 00:00:00',
                }
                queryset = TestOrm.objects.filter(**select_term)
                queryset = queryset.filter(user_id='yunsonbai')
                data = queryset.order_by('id').data()
        ```
        * function
            * limit
            * order_by
            * group_by
            * desc_order_by
            * first
            * all
            * count

        ##### Note
        ```python
            limit 要在 group_by/order_by 后边调用；
            每次查询语句(除去count)最后都要调用data才能查询出数据
        ```
        ##### Example
        ```python
            res = TestModel.objects.filter(**select_term).all().data()
            res = TestModel.objects.filter(**select_term).limit(0, 7).data()
            res = TestModel.objects.filter(
                    **select_term).order_by(id).limit(
                    0, 7).data()
        ```

	* Create Data
	##### Example
    ```python
    	def test_create_orm(i):
			create_data = {
				'label': 1,
				'title': 'test_{0}'.format(i)
			}
			TestOrm.create(**create_data)
    ```

    * Update Data
    ```python
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
    ```

    * Delete Data
    ```python
        def test_delete_orm():
			res = TestOrm.objects.filter(id__in=[7, ]).data()
			for r in res:
				result = r.delete()
				print(result)
    ```

* chart
	* create_sheet: 制作excel表格
	* 条形图: ![条形图](/example/text_curve.png)
	* 柱形图: ![条形图](/example/text.png)

* email
	* 发送出文本邮件: 请看example
	* 发送图片: 请看example
	* 发送附件: 请看example
