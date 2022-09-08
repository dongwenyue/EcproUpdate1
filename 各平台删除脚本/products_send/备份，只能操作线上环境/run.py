import os
import time
import sqlite3
import datetime
import sys


start_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')

tp_ids = sys.argv[1]
Product_Number = sys.argv[2]

# tp_ids = '天猫,淘宝'
Environment = 'pro'
# Product_Number = '0,455'
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
Environment_publish = 'on'
Versions = '3.0'
os.chdir('/root/yzm/products_publish/')
os.system('/usr/bin/python3  publish.py %s %s %s' % (Product_Name, Environment_publish, Versions))

# 等待上货完成
time.sleep(20)
end_time = (datetime.datetime.now() - datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')
print(end_time)
os.chdir('/root/yzm/products_send/')
os.system('/usr/bin/python3  sendmail_linux.py --start_time=%s --end_time=%s --tp_names=%s --product_name=%s' % ("'"+start_time+"'", "'"+end_time+"'", tp_ids, Product_Name))

# /usr/bin/python3  sendmail_linux.py --start_time=2022-03-17 07:09:50 --end_time=2022-03-18 07:09:50
# /usr/bin/python3  sendmail_linux.py --start_time='2022-03-17 07:09:50' --end_time='2022-03-18 07:09:50'

# 删除后台测试商品
os.chdir('/root/yzm/Delete/')
os.system('/usr/bin/python3  tm_ware_delete.py')
time.sleep(3)
os.system('/usr/bin/python3  jd_ware_delete.py')
time.sleep(3)
os.system('/usr/bin/python3  pdd_ware_delete.py')


