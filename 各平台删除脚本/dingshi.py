# -*- coding: utf-8 -*-
import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler


def job():
    os.system('/usr/bin/python3  /root/yzm/Delete/jd_ware_delete.py >> /root/yzm/Delete/jd.log')
    time.sleep(3)
    os.system('/usr/bin/python3  /root/yzm/Delete/tm_ware_delete.py >> /root/yzm/Delete/tm.log')
    time.sleep(3)
    os.system('/usr/bin/python3  /root/yzm/Delete/tiktok_ware_delete.py >> /root/yzm/Delete/tiktok.log')
    time.sleep(3)
    os.system('/usr/bin/python3  /root/yzm/Delete/pdd_ware_delete.py >> /root/yzm/Delete/pdd.log')
    time.sleep(3)
    os.system('/usr/bin/python3  /root/yzm/Delete/taobao_ware_delete.py >> /root/yzm/Delete/tb.log')
scheduler = BlockingScheduler()

scheduler.add_job(job, 'cron', day_of_week='1-6', hour='21', minute='30')

scheduler.start()
