# Project

目前从kuaidaili,xicidaili,7yip,ip3366,89ip,nimadaili,superfastip几个网站搜索代理ip。

增加或停止爬虫，修改plugin/setting.py文件中的pluginlist

项目启动文件是main.launch.py。

原计划是打算使用apscheduler作为调度器，但还没有摸清楚原理，因出现实例重新生成而使得内存使用过高。

当前存储在mongodb上的代理格式如下：
{
  "speed" : "0.5",
  "ipaddress" : "165.22.41.190",
  "availidtime" : "2020-03-17 00:36:15",
  "proxyid" : "10520f8fa81e228cf6950cce7ef3f007",
  "aliveminute" : 0,
  "svradd" : "中国 广东 韶关 电信",
  "isanony" : "高匿",
  "port" : "80",
  "frequency" : 30,
  "prototype" : "HTTP",
  "conntime" : ""
}

frequency为检测代理可用性为真的次数，上线为30，次数越高，说明该代理可用性越高。

