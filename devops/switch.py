#!/usr/bin/python
# coding:utf-8


import json
import psutil
import socket
import time
import re
import requests

def run():
    data = {'device': 'huawei-5710', 'ip': '192.168.10.10','cabinet': 1,'idc':1,'port':38}
    res = {}
    res['params']=data
    res['jsonrpc'] = "2.0"
    res["id"] = 1
    res["method"]= "switch.add"
 #   print res 
 #   for k,v in data.iteritems():
 #       print k, v
    send(res)

def send(data):
    url = "http://192.168.63.182:2000/api"
    r = requests.post(url, headers=headers,json=data)
    print r.status_code
    print r.content


if __name__ == "__main__":
   run()
