#!/usr/bin/env python
# coding=utf-8
import time
import random
import requests
from common.hander_random import requests_headers

headers = requests_headers()

def req_get(url, header_token=None):
    time.sleep(random.random()*5)
    try:
        if header_token:
            headers['token'] = header_token
        res = requests.get(url=url, headers=headers, verify=False, allow_redirects=False, timeout=(4,20))
        res.encoding = res.apparent_encoding # apparent_encoding比"utf-8"错误率更低
        return res
    except:
        print("\033[1;31mreq_get网络出错！\033[0m")
        pass

def req_post(url, data=None, header_token=None):
    try:
        if header_token:
            headers['token'] = header_token
        res = requests.post(url=url, headers=headers, verify=False, data=data, allow_redirects=False, timeout=(4,20))
        res.encoding = res.apparent_encoding # apparent_encoding比"utf-8"错误率更低
        return res
    except:
        print("\033[1;31mreq_post网络出错！\033[0m")
        pass