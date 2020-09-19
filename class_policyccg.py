# @Time : 2020/4/2 1:21 
# @Author : bufeetu
# @File : class_policyma.py 
import time, datetime
import os
import requests
import json
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from class_policy import Policy
#注释完毕
'''
主要多头逻辑:
如果持仓网格0,就委托a-x开多
如果a-x开多成功,更新开多时间戳,委托a平多.  然后等休眠时间超过且价格低于上次开多价格,再委托开多
如果持仓0,且价格超过最大委托价2x,就重新委托

'''

class Policyccg(Policy):
    def log(self,content):
        self.txt_write(self.coinname,self.dict_data['date']+'----'+str(self.dict_data['close'])+'----'+content)
    def init(self,coinname,param):
        self.coinname=coinname
        self.param=param
        self.mianzhi=self.get_mianzhi(coinname)
        self.list_wg=[]
        self.dict_acc={
            'money':10000,
            'last_wait_id':0,
            'last_open_id':0,
        }
        self.txt_remove(self.coinname + '.txt')
        #初始化网格id=0
        self.wgid=0
    def trade(self,id,status):
        for i in range(len(self.list_wg)):
            if self.list_wg[i]['id'] == id:
                self.list_wg[i]['status']=status
                if status=='duo_ok':
                    self.list_wg[i]['status'] = 'duo_closeing'
                    self.list_wg[i]['price_close'] =round(self.list_wg[i]['price'] + self.param['jiange'],3)
                if status=='duo_close':
                    self.list_wg[i]['date_close'] = self.dict_data['date']
                    self.list_wg[i]['shouyi'] =self.param['jiange']
                return True
        return False
    def weituo(self,price,zhangshu,status):
        self.wgid += 1
        dict_ls={
            'id':self.wgid,
            'price':round(price,3),
            'zhangshu':zhangshu,
            'status':status,
            'date':self.dict_data['date'],
            'price_close': 0,
            'date_close': 0,
            'shouyi': 0,
        }
        self.list_wg.append(dict_ls)
        self.dict_acc['last_wait_id']=dict_ls['id']
        self.log('委托成功,id'+str(dict_ls['id'])+status+',张数' + str(zhangshu) + '价格' + str(price))
    def get_ziduan_byid(self,id,ziduan):
        for i in range(len(self.list_wg)):
            if self.list_wg[i]['id'] == id:
                return self.list_wg[i][ziduan]
        return False
    def getid_price_min(self,status):
        res=0
        price=99999
        for i in range(len(self.list_wg)):
            if self.list_wg[i]['status'] == status and self.list_wg[i]['price']<price:
                price=self.list_wg[i]['price']
                res=self.list_wg[i]['id']
        return res
    def getid_price_max(self,status):
        res=0
        price=0
        for i in range(len(self.list_wg)):
            if self.list_wg[i]['status'] == status and self.list_wg[i]['price']>price:
                price=self.list_wg[i]['price']
                res=self.list_wg[i]['id']
        return res
    def run(self):
        price=self.dict_data['close']
        low=self.dict_data['low']
        high=self.dict_data['high']
        timechuo=self.dict_data['timechuo']
        zhangshu_chong=int(10000/self.mianzhi)
        zhangshu_dange=int(zhangshu_chong*self.param['zhangshu'])
        #低于最低持仓价格 且超过它的开仓休眠期,委托开多,且委托单为0
        id_price_min_duook=self.getid_price_min('duo_ok')
        id_price_max_duowait=self.getid_price_min('duo_wait')
        id_price_max_duocloseing=self.getid_price_min('duo_closeing')
        if id_price_max_duowait==0:#没有委托单
            #没有持仓单
            if id_price_min_duook == 0:
                self.log('开始委托多单,因为没有委托单,没有持仓单')
                self.weituo(price-self.param['jiange'],zhangshu_dange,'duo_wait')
                return
            #价格低于最低持仓价 且满足时间
            if price < self.get_ziduan_byid(id_price_min_duook, 'price') and timechuo - self.get_ziduan_byid(id_price_min_duook, 'timechuo') > self.param['sleep'] * 2:
                self.log('开始委托多单,因为没有委托单,价格'+str(price)+'低于最低持仓价格'+str(self.get_ziduan_byid(id_price_min_duook, 'price'))+'且不在休眠期')
                self.weituo(price - self.param['jiange'], zhangshu_dange, 'duo_wait')
                return
        else:
            # 撤单,高于最高委托价格2x价格
            if price-self.get_ziduan_byid(id_price_max_duowait,'price')>2*self.param['jiange']:
                self.log('撤销多单,因为价格'+str(price)+'高于最高委托价'+str(self.get_ziduan_byid(id_price_max_duowait,'price'))+'超出'+str(2*self.param['jiange']))
                self.trade(id_price_max_duowait,'duo_cancel')
                return
        # 开多成功,低于最高委托价格
        if low< self.get_ziduan_byid(id_price_max_duowait, 'price') and id_price_max_duowait>0:
            self.log('开多成功,因为low'+str(low)+'低于委托价格'+str(self.get_ziduan_byid(id_price_max_duowait, 'price')))
            self.trade(id_price_max_duowait, 'duo_ok')
            return
        # 平多成功,高于最高委托平仓价格
        if high>self.get_ziduan_byid(id_price_max_duocloseing,'price_close') and id_price_max_duocloseing>0:
            self.log('平多成功,因为high'+str(high)+'高于委托平仓价格'+str(self.get_ziduan_byid(id_price_max_duocloseing,'price_close')))
            self.trade(id_price_max_duocloseing, 'duo_close')
            return


    #初始化容器 遍历指定区间k线,调用run
    def start(self,coinname,date_start,date_end,param={}):
        self.init(coinname,param)
        # 遍历数据
        # path=os.path.abspath('.') + '/klineok/' + coinname + '1m1dok.csv'
        path=os.path.abspath(os.path.dirname(os.getcwd())) + '/klineok/' + coinname + '1m1dok.csv'
        path=os.path.abspath(os.path.dirname(os.getcwd())) + '/klineok/' + coinname + '1m1dok.csv'
        df_1m = pd.read_csv(path, index_col=0).reset_index()
        for i in range(len(df_1m)):
            timechuo=int(df_1m.loc[i, 'timechuo'])
            close= float(df_1m.loc[i, 'close'])
            ma60= float(df_1m.loc[i, 'ma60'])
            ma91= float(df_1m.loc[i, 'ma91'])
            self.dict_data = {
                'date': df_1m.loc[i, 'date'],
                'timechuo': int(df_1m.loc[i, 'timechuo']),
                'open': float(df_1m.loc[i, 'open']),
                'high': float(df_1m.loc[i, 'high']),
                'low': float(df_1m.loc[i, 'low']),
                'close': float(df_1m.loc[i, 'close']),
                'ddate': df_1m.loc[i, 'ddate'],
                'dvol':float(df_1m.loc[i, 'dvol']),
                'ma60': float(df_1m.loc[i, 'ma60']),
                'ma91': float(df_1m.loc[i, 'ma91']),
                'dc20up':float(df_1m.loc[i, 'dc20up']),
                'dc20dn': float(df_1m.loc[i, 'dc20dn']),
                'dc10up': float(df_1m.loc[i, 'dc10up']),
                'dc10dn':float(df_1m.loc[i, 'dc10dn']),
                'atr':float(df_1m.loc[i, 'atr']),
            }
            if timechuo > self.date_totimechuo(date_start) and timechuo< self.date_totimechuo(date_end):
                self.run()
            elif timechuo > self.date_totimechuo(date_end):
                break
            # if timechuo>self.date_totimechuo('2018-12-31 12:00') and self.dict_acc['money']<=100:
            #     self.txt_write('zongjie', 'fail'+str(self.dict_param))
            #     return
        # self.zongjie(quanyi=self.dict_acc['quanyi'],
        #              price=self.dict_data['close'],
        #              money=self.dict_acc['money'],
        #              fee_sum=self.dict_record['fee_sum'],
        #              date_start=date_start,
        #              date_end=date_end,
        #              huiche_max=max(self.dict_record['list_rate_huiche']))



