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

import os
from bs4 import BeautifulSoup
from plugin import setting
import copy
import requests
#import requests.packages.urllib3.util.ssl_
import time
import traceback
from main.loghandle import LogHandler as mylogger
import json
import random
import logging
logging.getLogger("requests").setLevel(logging.WARNING)

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

log = mylogger()

httpheader = {
    "User-Agent": "",
    "Host": "www.kuaidaili.com",
    "Accept": "text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/webp, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Accept-Encoding": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": None,
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
    
    for i in range(3):
        try:
            req = requests.get(url = proxyurl, headers = header, timeout = setting.timeout, verify = False)

            if req.status_code == 200:
                if req.text is not None:
                    soup = BeautifulSoup(req.text, "html.parser")
                    trs = soup.findAll("tr")
                    
                    for tr in trs:
                        try:
                            if len(tr.contents) <= 1:
                                continue
                            
                            if tr.contents[1].name == "th":
                                continue
                            
                            ip = tr.find("td", attrs = {"data-title": "IP"}).text
                            port = tr.find("td", attrs = {"data-title": "PORT"}).text
                            annoy = tr.find("td",  attrs = {"data-title": "匿名度"}).text
                            proxytype = tr.find("td", attrs = {"data-title": "类型"}).text
                            location = tr.find("td", attrs = {"data-title": "位置"}).text
                            resptim = tr.find("td", attrs = {"data-title": "响应速度"}).text
                            verfi = tr.find("td", attrs = {"data-title": "最后验证时间"}).text
                            
                            proxy = copy.deepcopy(setting.tmp_proxy)
                            proxy["ipaddress"] = ip
                            proxy["port"] = port
                            proxy["svradd"] = location
                            proxy["prototype"] = proxytype
                            proxy["isanony"] = annoy
                            proxy["speed"] = resptim
                            proxy["availidtime"] = verfi
                            
                            yield proxy
                        except Exception:
                            log.warning(traceback.format_exc())
                    return
            time.sleep(random.randint(0,5))
        except requests.exceptions.RequestException:
            # 连接超时
            log.warning(traceback.format_exc())
            continue
        except Exception:
            log.error(traceback.format_exc())

    return


# 启动爬虫
def run():
    #print("kuaidaili")
    httpheader["User-Agent"] = setting.getua()
    preurl = "https://www.kuaidaili.com"
    
    cookie = setting.getcookie(preurl, httpheader)
    
    iter = 0
    while cookie is None and iter < 10:
        cookie = setting.getcookie(preurl, httpheader)
        iter += 1
    
    if cookie is None:
        return 
    
    httpheader["Cookie"] = "; ".join(key + "=" + value for (key, value) in cookie.items())
    #httpheader["Cookie"] = httpheader["Cookie"][:-2]

    proxylsurl = ["https://www.kuaidaili.com/free/inha/", "https://www.kuaidaili.com/free/intr/"]
    #proxylsurl = ["https://www.kuaidaili.com/free/inha/"]
    
    for proxyurl in proxylsurl:
        
        for i in range(0, setting.pagerange):
    
            httpheader["Referer"] = preurl
            if i == 0:
                # page=1时的操作
                topurl = proxyurl
            else:
                topurl = proxyurl + str(i) + "/"
        
            time.sleep(setting.rate)
            log.info(os.path.split(__file__)[1] + " processing " + topurl)
            for proxy in singleproxy(topurl, httpheader):
                yield proxy 
    
            preurl = topurl


if __name__ == "__main__":
    proxies = run()
    for proxy in proxies:
        print(proxy)
        print(json.dumps(proxy, ensure_ascii = False))
        log.LOG(action = "info", msg = json.dumps(proxy, ensure_ascii = False))
    
    
