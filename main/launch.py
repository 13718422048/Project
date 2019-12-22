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

from apscheduler.schedulers.blocking import BlockingScheduler


def job1(text):
	print("job1 " + text)

def job2(text):
	print("job2 " + text)

if __name__ == "__main__":
	
	"""scheduler = BlockingScheduler()
	scheduler.add_job(job1, "date", run_date = '2019-11-17 00:05:00', args=["测试dddddddd"])
	scheduler.add_job(job2, "date", run_date = '2019-11-17 00:06:00', args=["测试ddd"])
	
	scheduler.start()"""
	string_ip = "is this 233.22.22.22 ip ?"
	result = re.findall(r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b", string_ip)
	if result is None:
		print(result)




