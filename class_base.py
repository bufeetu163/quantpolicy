import time, datetime
import os
import requests
import json
import urllib
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
class Base():

    #基础通用方法

    def timechuo_getzerotimechuo(self, timechuo):
        zero_timechuo = int(timechuo - (timechuo % 86400))+3600*16
        return zero_timechuo
    def timechuo_todate(self, timechuo):
        date = time.strftime("%Y-%m-%d %H:%M", time.localtime(int(timechuo)))
        return date
    def date_totimechuo(self,data="2013-10-10 23:40"):
        timeArray = time.strptime(data, "%Y-%m-%d %H:%M")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp
    def get_date_now(self):
        res=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return res
    def txt_write(self,filename,content):
        with open(filename+".txt", "a+") as f:
            f.write(content+'\n')
            print(content)
    def txt_remove(self,filename):
        if os.path.exists(filename):
            os.remove(filename)


    #基础网络请求
    def get_url(self, url):
        add_to_headers = None
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        try:
            response = requests.get(url, params=None, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "fail"}
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return {"status": "fail", "msg": "%s" % e}
    def http_get_request(self, url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        try:
            response = requests.get(url, postdata, headers=headers, timeout=30)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "fail"}
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return {"status": "fail", "msg": "%s" % e}

