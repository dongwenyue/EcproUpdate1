# -*- coding: UTF-8 -*-
import os
import time
import sqlite3
import datetime
import sys


start_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

tp_ids = sys.argv[1]
Product_Number = sys.argv[2]
Environment = sys.argv[3]
# tp_ids = '天猫,淘宝'
# Product_Number = '0,455'
# Environment = 'pro'
pattern = 'Product_Fields'

# 切换python的工作目录
os.chdir('/root/yzm/ECProExport3_mul/ECProExport/resource/dbs/')
os.system('/usr/bin/python3 update_sqlite3_linux.py %s %s' % (tp_ids, Environment))

os.chdir('/root/yzm/ECProExport3_mul/ECProExport/')
os.system('/usr/bin/python3 runTest_linux.py %s %s %s' % (Environment, Product_Number, pattern))


db_path = '/root/yzm/ECProExport3_mul/ECProExport/resource/dbs/Case.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
sql = "SELECT codes FROM createProduct"
cursor.execute(sql)
result = cursor.fetchone()
conn.close()
print(result[0][:6])


Product_Name = result[0][:6]
if Environment == 'pro':
    Environment_publish = 'on'
elif Environment == 'beta':
    Environment_publish = 'qa'
Versions = '3.0'
os.chdir('/root/yzm/products_publish/')
os.system('/usr/bin/python3  publish.py %s %s %s' % (Product_Name, Environment_publish, Versions))

# 等待的时间间隔，不对，因为有的还在上货中，但时间已经过了20秒
# 等待上货完成
# for i in range(30):
#     print('time dao ji shi', i)
#     time.sleep(1)
print("publish.created_at等待的时间间隔1分钟")
end_time = (datetime.datetime.now() - datetime.timedelta(hours=8) + datetime.timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')
print('开始时间', start_time)
print('结束时间', end_time)
time.sleep(2)
os.chdir('/root/yzm/products_send/')
print('/usr/bin/python3  sendmail_linux.py --start_time=%s --end_time=%s --tp_names=%s --product_name=%s --Environment=%s' % ("'"+start_time+"'", "'"+end_time+"'", tp_ids, Product_Name, Environment))

os.system('/usr/bin/python3  sendmail_linux.py --start_time=%s --end_time=%s --tp_names=%s --product_name=%s --Environment=%s' % ("'"+start_time+"'", "'"+end_time+"'", tp_ids, Product_Name, Environment))

# /usr/bin/python3  sendmail_linux.py --start_time=2022-03-17 07:09:50 --end_time=2022-03-18 07:09:50
# /usr/bin/python3  sendmail_linux.py --start_time='2022-03-17 07:09:50' --end_time='2022-03-18 07:09:50'

# 删除后台测试商品
# os.chdir('/root/yzm/Delete/')
# os.system('/usr/bin/python3  tm_ware_delete.py')
# time.sleep(3)
# os.system('/usr/bin/python3  jd_ware_delete.py')
# time.sleep(3)
# os.system('/usr/bin/python3  pdd_ware_delete.py')




