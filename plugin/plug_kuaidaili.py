#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2019/11/3
"""

'''
function : kuaidaili站点的爬虫(https://www.kuaidaili.com)
'''


from bs4 import BeautifulSoup
import setting
import copy
import requests
import re
import time
import traceback

httpheader = {
    "User-Agent": "",
    "Host": "www.kuaidaili.com",
    "Accept": "text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": "",
    "Cookie": None,
    "Cache-Control": "no-cache",
    "Connection": "Keep-Alive",
    "DNT": "1"
}


"""# 单个列表页面
def proxylist(topurl, header):
    '''
    function: 获取单个页面上，各代理详情页的url
    paras: url, 单个代理页面的url
    return: <iter>
    '''

    #htmler = request.urlopen(url, data=None, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, cafile=None, capath=None, cadefault=False, context=None)

    req = requests.get(url = topurl, header = header, timeout = 5)
    if req.status_code == 200:
		soup = BeautifulSoup(req.text, "html.parser")
		hrefas = soup.findAll("a", href = re.compile(r'/dayProxy/ip/[0-9]+\.html'))
		for href in hrefas:
			yield href["href"]
"""

# 内容页
def singleproxy(proxyurl, header):
    req = requests.get(url = proxyurl, header = header, timeout = 5)
    if req.status_code == 200:
	soup = BeautifulSoup(req.text, "html.parser")
	trs = soup.findAll(name="tr")
	
	for tr in trs:
		try:
			ip = tr.find("td", data-title="IP").text
			port = tr.find("td", data-title="PORT").text
			annoy = tr.find("td", data-title="匿名度").text
			proxytype = tr.find("td", data-title="类型").text
			location = tr.find("td", data-title="位置").text
			resptim = tr.find("td", data-title="响应速度").text
			verfi = tr.find("td", data-title="最后验证时间").text
			
			proxy = copy.deepcopy(setting.tmp_proxy)
			proxy["ipaddress"] = ip
			proxy["port"] = port
			proxy["serveradd"] = location
			proxy["prototype"] = proxytype
			proxy["isanony"] = annoy
			proxy["speed"] = resptim
			proxy["availidtime"] = verfi
			
			yield proxy
		except Exception as e:
			traceback.print_exc()
		
		
# 翻页
def pagelist():

    pass

# 启动爬虫
def run():
	httpheader["User-Agent"] = setting.getua()
	preurl = "https://www.kuaidaili.com"
	
	cookie = setting.getcookie(preurl, httpheader)
	
	httpheader["Cookie"] = "; ".join(key + "=" + value for key, value in cookie.iteritems())

	proxylsurl = ["https://www.kuaidaili.com/free/inha/", "https://www.kuaidaili.com/free/intr/"]
	
	for proxyurl in proxylsurl:
		
		for i in range(0, setting.pagerange):
	
			httpheader["Referer"] = preurl
			if i == 0:
				# page=1时的操作
				topurl = proxyurl
			else:
				topurl = proxyurl + str(i) + "/"
		
			time.sleep(setting.rate)
			yield pagelist(topurl, httpheader)
	
			preurl = topurl


if __name__ == "__main__":

    url = "https://www.baidu.com"
    httpheader["Host"] = "www.baidu.com"

    httpheader["User-agent"] = setting.getua()
    req = requests.get(url, headers = httpheader)
    for key,value in req.cookies.iteritems():
	print("{0}:{1}".format(key,value))

    print(req.cookies.items())
