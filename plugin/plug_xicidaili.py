# coding: utf-8


'''
function: 西刺代理
'''

from bs4 import BeautifulSoup
import requests
import time
import copy
import setting
import random


httpheader = {
    "Host" : "www.xicidaili.com",
    "User-Agent" : "",
    "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language" : "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding" : "gzip, deflate, br",
    "DNT" : "1",
    "Connection" : "keep-alive",
    "Cookie" : None,
    "Upgrade-Insecure-Requests" : "1",
    "If-None-Match" : "W/\"38bfd3249573a8d3b1ff9301bad1bdff"
}


# 需要获取If-None-Match

def extractlabel(soup, label , attr):
    trs = soup.findAll(label, _class = attr)
    
    for tr in trs:
        tds = list(tr.children)
        
        ip = BeautifulSoup(tds[1], "html.parser").find("td").string
        port = BeautifulSoup(tds[2], "html.parser").find("td").string
        svradd = BeautifulSoup(tds[3], "html.parser").find("a").string
        isannoy = BeautifulSoup(tds[4], "html.parser").find("td").string
        prototype = BeautifulSoup(tds[5], "html.parser").find("td").string
        speed = (BeautifulSoup(tds[6], "html.parser").find("div", class_ = "bar").get("title")).replace("秒", "")
        conntime = (BeautifulSoup(tds[7], "html.parser").find("div", class_ = "bar").get("title")).replace("秒", "")
        livetime = BeautifulSoup(tds[8], "html.parser").find("td").string
        validatime = BeautifulSoup(tds[9], "html.parser").find("td").string
        
        """ip = tds[1].td.string
        port = tds[2].td.string
        svradd = tds[3].a.string
        isannoy = tds[4].td.string
        prototype = tds[5].td.string 
        speed = (tds[6].find("div", class_ = "bar").get("title")).replace("秒", "")
        conntime = (tds[7].find("div", class_ = "bar").get("title")).replace("秒", "")
        livetime = tds[8].td.string
        validatime = tds[9].td.string"""
        
        yield (ip, port, svradd, isannoy, prototype, speed, conntime, livetime, validatime)

def getproxy(url, header):
    res = requests.get(url, header = header)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")
        
        for attr in ["", "odd"]:
            for cc in extractlabel(soup, "tr", attr):
                proxy = copy.deepcopy(setting.tmp_proxy)
                proxy["ipaddress"] = cc[0]
                proxy["port"] = cc[1]
                proxy["serveradd"] = cc[2]
                proxy["isanony"] = cc[3]
                proxy["prototype"] = cc[4]
                proxy["speed"] = cc[5]
                proxy["conntime"] = cc[6]
                proxy["aliveminute"] = cc[7]
                proxy["availidtime"] = cc[8]
            
                yield proxy
        
def run():    
    preurl = "https://www.xicidaili.com"
    # getcookie & getua
    proxyurl = ["https://www.xicidaili.com/nn/", "https://www.xicidaili.com/nt/", "https://www.xicidaili.com/wn/", "https://www.xicidaili.com/wt/"]
    httpheader["User-Agent"] = setting.getua()
    cookie = setting.getcookie(preurl, httpheader)
    
    for url in proxyurl:
        iterurl = ""
        for i in range(10):
            if i == 0:
                iterurl = url
            else:
                iterurl = url + str(i)
            
            time.sleep(setting.rate)
            yield getproxy(iterurl, httpheader)
    pass


if __name__ == "__main__":
    pass


