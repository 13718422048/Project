#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/7/7
"""

# 模块
# 1. 搜集代理ip
# 2. 验证代理ip有效性
# 3. 存储ip到数据库

#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

from main.spider import run as spiderrun
from main.proxyvalidate import refresh as refreshproxy
from main.proxyvalidate import filter as filterproxy

from gevent import monkey
monkey.patch_all(thread = False, multiprocessing = False)    

import time
import threading
import multiprocessing

def job1(func, interval):
    print(str(func.__name__) + " sleep {0}s".format(interval))
    func(interval)

def job2(func, interval):
    while True:
        print(str(func.__name__) + " sleep {0}s".format(interval))
        time.sleep(interval)
        func()
        
def run():
    #scheduler = BackgroundScheduler()
    scheduler = BlockingScheduler()
    # 每小时获取一次代理
    scheduler.add_job(spiderrun, "interval", minutes = 10, coalesce = True, misfire_grace_time = 300)
    #scheduler.add_job(spiderrun, trigger = "date", run_date = "2020-03-10 19:53:00")
    # 每分钟验证当前可用代理
    scheduler.add_job(refreshproxy, "interval", minutes = 1, coalesce = True, misfire_grace_time = 60)
    # 每十分钟过滤一遍代理
    scheduler.add_job(filterproxy, "interval", minutes = 5, coalesce = True, misfire_grace_time = 300)
    
    scheduler.start()


if __name__ == "__main__":
    
    funcs = [(spiderrun, 7200), (refreshproxy, 60), (filterproxy, 300)]
    #funcs = [ (refreshproxy, 60), (filterproxy, 300)]
    
    pool = multiprocessing.Pool(processes = len(funcs))
#     for funcpara in funcs:
#         pool.apply_async(job2, funcpara)
    
    pool.apply_async(job2, funcs[0])
    for i in range(1,len(funcs)):
        pool.apply_async(job1, funcs[i])
    
    pool.close()
    pool.join()
    print("end")
#     run()
    
