#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 20180917
# @Author  : zhaobo
# @github  :
import time
import base64
import hmac
import hashlib
import json
import urllib
import datetime
import requests
'''
ACCESS_KEY = 'bb744223-32147a86-56597f7f-ez2xc4vb6n'
SECRET_KEY = '8bc9bf60-64d68dfc-2cc3f4f7-b08de'
dm = HuobiDM(URL, ACCESS_KEY, SECRET_KEY)
dm.order_piliang(
        coinname='btc',
        price_start=11550,
        jiange=20,
        times=40,
        volume=1,
        direction='sell',
        offset='open',
        jingdu=2,
        lever_rate=10
    )
'''
class HuobiDM:

    def __init__(self,access_key,secret_key):
        self.__url = 'https://api.btcgateway.pro'
        self.__access_key = access_key
        self.__secret_key = secret_key

    def order_piliang(self, coinname, price_start, jiange, times, volume, direction, offset,contract_type='next_quarter',lever_rate=10):
        jingdu=self.get_jingdu(coinname)
        i = 1
        while i <= times:
            if offset=='open':
                if direction=='buy':
                    print('批量开多')
                    price = price_start - i * jiange
                else:
                    print('批量开空')
                    price = price_start + i * jiange
            else:
                if direction=='buy':
                    print('批量平空')
                    price = price_start - i * jiange
                else:
                    print('批量平多')
                    price = price_start + i * jiange
            price = round(price, jingdu)
            print('执行,i=' + str(i) + '价格' + str(price))
            i = i + 1
            res = self.send_contract_order(symbol=coinname, price=price, volume=volume, direction=direction,
                                           offset=offset,lever_rate=lever_rate,contract_type=contract_type)
            print(res)
    # 获取合约信息
    # def get_contract_info(self, symbol='', contract_type='', contract_code=''):
    #     """
    #     参数名称         参数类型  必填    描述
    #     symbol          string  false   "BTC","ETH"...
    #     contract_type   string  false   合约类型: this_week:当周 next_week:下周 quarter:季度
    #     contract_code   string  false   BTC181228
    #     备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
    #     """
    #     params = {}
    #     if symbol:
    #         params['symbol'] = symbol
    #     if contract_type:
    #         params['contract_type'] = contract_type
    #     if contract_code:
    #         params['contract_code'] = contract_code
    #
    #     url = self.__url + '/api/v1/contract_contract_info'
    #     return http_get_request(url, params)
    # # 获取合约指数信息
    # def get_contract_index(self, symbol):
    #     """
    #     :symbol    "BTC","ETH"...
    #     """
    #     params = {'symbol': symbol}
    #
    #     url = self.__url + '/api/v1/contract_index'
    #     return http_get_request(url, params)
    # # 获取合约最高限价和最低限价
    # def get_contract_price_limit(self, symbol='', contract_type='', contract_code=''):
    #     """
    #     :symbol          "BTC","ETH"...
    #     :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
    #     "contract_code   BTC180928
    #     备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
    #     """
    #     params = {}
    #     if symbol:
    #         params['symbol'] = symbol
    #     if contract_type:
    #         params['contract_type'] = contract_type
    #     if contract_code:
    #         params['contract_code'] = contract_code
    #
    #     url = self.__url + '/api/v1/contract_price_limit'
    #     return http_get_request(url, params)
    # # 获取当前可用合约总持仓量
    # def get_contract_open_interest(self, symbol='', contract_type='', contract_code=''):
    #     """
    #     :symbol          "BTC","ETH"...
    #     :contract_type   合约类型: this_week:当周 next_week:下周 quarter:季度
    #     "contract_code   BTC180928
    #     备注：如果contract_code填了值，那就按照contract_code去查询，如果contract_code 没有填值，则按照symbol+contract_type去查询
    #     """
    #     params = {'symbol': symbol,
    #               'contract_type': contract_type,
    #               'contract_code': contract_code}
    #
    #     url = self.__url + '/api/v1/contract_open_interest'
    #     return http_get_request(url, params)
    #
    #
    # # 获取行情深度
    # def get_contract_depth(self, symbol, type):
    #     """
    #     :param symbol:   BTC_CW, BTC_NW, BTC_CQ , ...
    #     :param type: 可选值：{ step0, step1, step2, step3, step4, step5 （合并深度0-5）；step0时，不合并深度 }
    #     :return:
    #     """
    #     params = {'symbol': symbol,
    #               'type': type}
    #
    #     url = self.__url + '/market/depth'
    #     return http_get_request(url, params)
    # # 获取KLine
    # def get_contract_kline(self, symbol, period, size=150):
    #     """
    #     :param symbol  BTC_CW, BTC_NW, BTC_CQ , ...
    #     :param period: 可选值：{1min, 5min, 15min, 30min, 60min, 4hour, 1day, 1week, 1mon }
    #     :param size: [1,2000]
    #     :return:
    #     """
    #     params = {'symbol': symbol,
    #               'period': period}
    #     if size:
    #         params['size'] = size
    #
    #     url = self.__url + '/market/history/kline'
    #     return http_get_request(url, params)
    # # 获取聚合行情
    # def get_contract_market_merged(self, symbol):
    #     """
    #     :symbol	    "BTC_CW","BTC_NW", "BTC_CQ" ...
    #     """
    #     params = {'symbol': symbol}
    #
    #     url = self.__url + '/market/detail/merged'
    #     return http_get_request(url, params)
    # # 获取市场最近成交记录
    # def get_contract_trade(self, symbol, size=1):
    #     """
    #     :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }
    #     :return:
    #     """
    #     params = {'symbol': symbol,
    #               'size' : size}
    #
    #     url = self.__url + '/market/trade'
    #     return http_get_request(url, params)
    # # 批量获取最近的交易记录
    # def get_contract_batch_trade(self, symbol, size=1):
    #     """
    #     :param symbol: 可选值：{ BTC_CW, BTC_NW, BTC_CQ, etc. }, size: int
    #     :return:
    #     """
    #     params = {'symbol': symbol,
    #               'size' : size}
    #
    #     url = self.__url + '/market/history/trade'
    #     return http_get_request(url, params)
    # # 获取用户账户信息
    # def get_contract_account_info(self, symbol=''):
    #     """
    #     :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
    #     :return:
    #     """
    #
    #     params = {}
    #     if symbol:
    #         params["symbol"] = symbol
    #
    #     request_path = '/api/v1/contract_account_info'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 获取用户持仓信息
    # def get_contract_position_info(self, symbol=''):
    #     """
    #     :param symbol: "BTC","ETH"...如果缺省，默认返回所有品种
    #     :return:
    #     """
    #
    #     params = {}
    #     if symbol:
    #         params["symbol"] = symbol
    #
    #     request_path = '/api/v1/contract_position_info'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # 合约下单

    def get_jingdu(self,coinname):
        coinname=str(coinname).lower()
        if coinname=='btc':
            jingdu=2
        elif coinname=='link' or coinname=='xrp':
            jingdu = 4
        elif coinname=='trx':
            jingdu = 5
        elif coinname=='ada':
            jingdu = 6
        else:
            jingdu=3
        return jingdu
    def send_contract_order(self, symbol, price, volume, direction, offset,lever_rate,contract_type):
        params = {
            # 'contract_type': "next_quarter",
            # 'contract_type': "quarter",
            'contract_type': contract_type,
            "direction": direction,
            "lever_rate": lever_rate,
            "offset": offset,
            "order_price_type": "limit",
            "price": price,
            "symbol": str(symbol).upper(),
            "volume": volume,
        }
        request_path = '/api/v1/contract_order'
        print(params)
        res = self.api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
        return res
    # # 合约批量下单
    # def send_contract_batchorder(self, orders_data):
    #     """
    #     orders_data: example:
    #     orders_data = {'orders_data': [
    #            {'symbol': 'BTC', 'contract_type': 'quarter',
    #             'contract_code':'BTC181228',  'client_order_id':'',
    #             'price':1, 'volume':1, 'direction':'buy', 'offset':'open',
    #             'leverRate':20, 'orderPriceType':'limit'},
    #            {'symbol': 'BTC','contract_type': 'quarter',
    #             'contract_code':'BTC181228', 'client_order_id':'',
    #             'price':2, 'volume':2, 'direction':'buy', 'offset':'open',
    #             'leverRate':20, 'orderPriceType':'limit'}]}
    #
    #     Parameters of each order: refer to send_contract_order
    #     """
    #
    #     params = orders_data
    #     request_path = '/api/v1/contract_batchorder'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 撤销订单
    # def cancel_contract_order(self, symbol, order_id='', client_order_id=''):
    #     """
    #     参数名称          是否必须 类型     描述
    #     symbol           true   string  BTC, ETH, ...
    #     order_id	         false  string  订单ID（ 多个订单ID中间以","分隔,一次最多允许撤消50个订单 ）
    #     client_order_id  false  string  客户订单ID(多个订单ID中间以","分隔,一次最多允许撤消50个订单)
    #     备注： order_id 和 client_order_id都可以用来撤单，同时只可以设置其中一种，如果设置了两种，默认以order_id来撤单。
    #     """
    #
    #     params = {"symbol": symbol}
    #     if order_id:
    #         params["order_id"] = order_id
    #     if client_order_id:
    #         params["client_order_id"] = client_order_id
    #
    #     request_path = '/api/v1/contract_cancel'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 全部撤单
    # def cancel_all_contract_order(self, symbol):
    #     """
    #     symbol: BTC, ETH, ...
    #     """
    #
    #     params = {"symbol": symbol}
    #
    #     request_path = '/api/v1/contract_cancelall'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 获取合约订单信息
    # def get_contract_order_info(self, symbol, order_id='', client_order_id=''):
    #     """
    #     参数名称	        是否必须	类型	    描述
    #     symbol          true    string  BTC, ETH, ...
    #     order_id	        false	string	订单ID（ 多个订单ID中间以","分隔,一次最多允许查询20个订单 ）
    #     client_order_id	false	string	客户订单ID(多个订单ID中间以","分隔,一次最多允许查询20个订单)
    #     备注：order_id和client_order_id都可以用来查询，同时只可以设置其中一种，如果设置了两种，默认以order_id来查询。
    #     """
    #
    #     params = {"symbol": symbol}
    #     if order_id:
    #         params["order_id"] = order_id
    #     if client_order_id:
    #         params["client_order_id"] = client_order_id
    #
    #     request_path = '/api/v1/contract_order_info'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 获取合约订单明细信息
    # def get_contract_order_detail(self, symbol, order_id, order_type, created_at, page_index=None, page_size=None):
    #     """
    #     参数名称     是否必须  类型    描述
    #     symbol      true	    string "BTC","ETH"...
    #     order_id    true	    long	   订单id
    #     order_type  true    int    订单类型。1:报单， 2:撤单， 3:爆仓， 4:交割
    #     created_at  true    number 订单创建时间
    #     page_index  false   int    第几页,不填第一页
    #     page_size   false   int    不填默认20，不得多于50
    #     """
    #
    #     params = {"symbol": symbol,
    #               "order_id": order_id,
    #               "order_type": order_type,
    #               "created_at": created_at}
    #     if page_index:
    #         params["page_index"] = page_index
    #     if page_size:
    #         params["page_size"] = page_size
    #
    #     request_path = '/api/v1/contract_order_detail'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    #
    # # 获取合约当前未成交委托
    # def get_contract_open_orders(self, symbol=None, page_index=None, page_size=None):
    #     """
    #     参数名称     是否必须  类型   描述
    #     symbol      false   string "BTC","ETH"...
    #     page_index  false   int    第几页,不填第一页
    #     page_size   false   int    不填默认20，不得多于50
    #     """
    #
    #     params = {}
    #     if symbol:
    #         params["symbol"] = symbol
    #     if page_index:
    #         params["page_index"] = page_index
    #     if page_size:
    #         params["page_size"] = page_size
    #
    #     request_path = '/api/v1/contract_openorders'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)
    # # 获取合约历史委托
    # def get_contract_history_orders(self, symbol, trade_type, type, status, create_date,
    #                                 page_index=None, page_size=None):
    #     """
    #     参数名称     是否必须  类型     描述	    取值范围
    #     symbol      true	    string  品种代码  "BTC","ETH"...
    #     trade_type  true	    int     交易类型  0:全部,1:买入开多,2: 卖出开空,3: 买入平空,4: 卖出平多,5: 卖出强平,6: 买入强平,7:交割平多,8: 交割平空
    #     type        true	    int     类型     1:所有订单、2：结束汏订单
    #     status      true	    int     订单状态  0:全部,3:未成交, 4: 部分成交,5: 部分成交已撤单,6: 全部成交,7:已撤单
    #     create_date true	    int     日期     7，90（7天或者90天）
    #     page_index  false   int     页码，不填默认第1页
    #     page_size   false   int     不填默认20，不得多于50
    #     """
    #
    #     params = {"symbol": symbol,
    #               "trade_type": trade_type,
    #               "type": type,
    #               "status": status,
    #               "create_date": create_date}
    #     if page_index:
    #         params["page_index"] = page_index
    #     if page_size:
    #         params["page_size"] = page_size
    #
    #     request_path = '/api/v1/contract_hisorders'
    #     return api_key_post(self.__url, request_path, params, self.__access_key, self.__secret_key)

    # 各种请求,获取数据方式
    def http_get_request(self,url, params, add_to_headers=None):
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:53.0) Gecko/20100101 Firefox/53.0'
        }
        if add_to_headers:
            headers.update(add_to_headers)
        postdata = urllib.parse.urlencode(params)
        try:
            response = requests.get(url, postdata, headers=headers, timeout=5)
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
            response = requests.post(url, postdata, headers=headers, timeout=5)
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





