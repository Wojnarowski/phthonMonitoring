#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql

# 打开数据库连接
db = pymysql.connect(".com", "root", "root", "db_aa", charset='utf8' )

# 使用cursor()方法获取操作游标
cursor = db.cursor()

# SQL 更新语句
sql = "update deposit_product set reserve2=0 where product_id= 4001"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 提交到数据库执行
   db.commit()
except:
   # 发生错误时回滚
   db.rollback()

# 关闭数据库连接
db.close()
