import time, datetime
import os
import requests
import json
import urllib
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_columns', None)
import numpy as np
import base64
import hmac
import hashlib

class Base():

    #基础日期操作
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
    #基础文本操作
    def txt_write(self,filename,content):
        print(content)
        with open(filename+".txt", "a+") as f:
            f.write(content+'\n')
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
    #火币的基础请求
    def http_get_request(self,url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        try:
            response = requests.get(url, postdata, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return {"status": "fail"}
        except Exception as e:
            print("httpGet failed, detail is:%s" % e)
            return {"status": "fail", "msg": "%s" % e}

    def http_post_request(self,url, params, add_to_headers=None):
        headers = {
            "Accept": "application/json",
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = json.dumps(params)
        try:
            response = requests.post(url, postdata, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                return response.json()
        except Exception as e:
            print("httpPost failed, detail is:%s" % e)
            return {"status": "fail", "msg": "%s" % e}

    def api_key_get(self,url, request_path, params, ACCESS_KEY, SECRET_KEY):
        method = 'GET'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params.update({'AccessKeyId': ACCESS_KEY,
                       'SignatureMethod': 'HmacSHA256',
                       'SignatureVersion': '2',
                       'Timestamp': timestamp})

        host_name = host_url = url
        # host_name = urlparse.urlparse(host_url).hostname
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()

        params['Signature'] = self.createSign(params, method, host_name, request_path, SECRET_KEY)
        url = host_url + request_path
        return self.http_get_request(url, params)

    def api_key_post(self,url, request_path, params, ACCESS_KEY, SECRET_KEY):
        method = 'POST'
        timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        params_to_sign = {'AccessKeyId': ACCESS_KEY,
                          'SignatureMethod': 'HmacSHA256',
                          'SignatureVersion': '2',
                          'Timestamp': timestamp}

        host_url = url
        # host_name = urlparse.urlparse(host_url).hostname
        host_name = urllib.parse.urlparse(host_url).hostname
        host_name = host_name.lower()
        params_to_sign['Signature'] = self.createSign(params_to_sign, method, host_name, request_path, SECRET_KEY)
        url = host_url + request_path + '?' + urllib.parse.urlencode(params_to_sign)
        return self.http_post_request(url, params)

    def createSign(self,pParams, method, host_url, request_path, secret_key):
        sorted_params = sorted(pParams.items(), key=lambda d: d[0], reverse=False)
        encode_params = urllib.parse.urlencode(sorted_params)
        payload = [method, host_url, request_path, encode_params]
        payload = '\n'.join(payload)
        payload = payload.encode(encoding='UTF8')
        secret_key = secret_key.encode(encoding='UTF8')
        digest = hmac.new(secret_key, payload, digestmod=hashlib.sha256).digest()
        signature = base64.b64encode(digest)
        signature = signature.decode()
        return signature

