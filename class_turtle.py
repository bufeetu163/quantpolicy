# -*- coding: utf-8 -*-
# @Time    : 2020/7/28 15:16
# @Author  : bufeetu
# @FileName: class_turtle.py
# @Software: PyCharm
import os
import requests
import json
import urllib
import time, datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
from class_base import Base
'''
根据起始时间 截止时间，从base获取整合好的分钟数据 小时数据，遍历数据

定义一个账户字典   空的list存储交易数据
#
'''
class Turtle(Base):
    def zongjie(self):
        #导出日志列表
        df = pd.DataFrame(self.log_list)
        df.to_csv(self.coinname+'log.csv', encoding="utf_8_sig")
    def log(self,command,price='', volume=''):
        m=str(self.data['date'])+'------------'+command+'价格'+str(price)+'张数'+str(volume)+'理由'+self.reason
        log_dict={
            'command':command,
            'price':price,
            'volume':volume,
            'reason':self.reason,
            'date':str(self.data['date']),
        }
        self.txt_write(self.coinname,m)
        if command.find('止盈')!=-1 or command.find('止损')!=-1:
            self.txt_write(self.coinname, '')
            self.txt_write(self.coinname, '')
            self.txt_write(self.coinname, '')
        # self.log_list.append(log_dict)
    def get_weijiesuan(self):
        pass
    def get_unit(self,margin_balance,price,atr,mianzhi):
        fund=margin_balance*price
        unit_coin=fund*0.01/atr
        unit_zhangshu=round(unit_coin*price*10/mianzhi,2)
        return int(unit_zhangshu)
    def trade(self,price,volume,offset,direction,command=''):
        if command=='buy':
            self.account['margin_balance'] = self.account['usdt'] / price
            self.account['usdt'] = 0
            self.log(command, price, self.account['margin_balance'])
            return
        if offset=='open':
            if direction=='chong':
                #初始化次数和最新价格
                self.account['times_open'] = 0
                self.account['priceopen_last'] = 0
                self.account['volume_chong'] += volume
                self.log('开冲', price, volume)
            else:
                #增加次数 更新最新价格
                self.account['times_open'] += 1
                self.account['priceopen_last'] = price
                if direction == 'buy':
                    self.account['volume_duo'] += volume
                    self.log('开多', price, volume)
                else:
                    self.account['volume_kong'] += volume
                    self.log('开空', price, volume)
            row = {
                'price': price,
                'volume': volume,
                'direction': direction,  # buy sell
                'offset': offset,  # open close
                'date': self.data['date'],
                'fee': 0,
                'shouyi': 0,
                'rate_shouyi': 0,
            }
            self.trade_list.append(row)
        else:
            # 更新次数和最新价格
            self.account['times_open'] = 0
            self.account['priceopen_last'] = 0
            if direction=='buy':
                self.log(command, price, self.account['volume_kong'])
            elif direction=='sell':
                self.log(command, price, self.account['volume_duo'])
            #清空记录
            self.account['volume_duo'] = 0
            self.account['volume_kong'] = 0
            self.account['volume_chong']=0
            self.trade_list = []

    def get_command(self):
        price=self.data['close']
        ma91=self.data['ma91']
        dc10up=self.data['dc10up']
        dc10dn=self.data['dc10dn']
        dc20up = self.data['dc20up']
        dc20dn = self.data['dc20dn']
        atr = self.data['atr']
        if self.account['usdt'] == 10000 and self.account['margin_balance']==0:
            return 'buy'
        if self.account['volume_chong']==0:
            self.reason='冲单0'
            return 'duichong'
        if price>ma91:
            if self.account['volume_kong']>0:
                self.reason = 'price>ma91'
                return 'zhisunkong'
            if self.account['times_open']==0:
                if price>dc20up:
                    self.reason = 'price>dc20up'
                    return 'openduo'
            else:
                if price>self.account['priceopen_last'] + 0.5 * atr:
                    self.reason = 'price>priceopen_last+0.5atr'
                    return 'addduo'
                elif price<dc10up:
                    self.reason = 'price<dc10up'
                    return 'zhiyingduo'
                elif price<self.account['priceopen_last'] - 2 * atr:
                    self.reason = 'price<priceopen_last-2atr'
                    return 'zhisunduo'
        else:
            if self.account['volume_duo']>0:
                self.reason = 'price<ma91'
                return 'zhisunduo'
            if self.account['times_open']==0:
                if price<dc20dn:
                    self.reason = 'price<dc20dn'
                    return 'openkong'
            else:
                if price<self.account['priceopen_last'] - 0.5 * atr:
                    self.reason = 'price<priceopen_last-0.5atr'
                    return 'addkong'
                elif price>dc10dn:
                    self.reason = 'price>dc10dn'
                    return 'zhiyingkong'
                elif price>self.account['priceopen_last'] + 2 * atr:
                    self.reason = 'price>priceopen_last+2atr'
                    return 'zhisunkong'
        return ''
    def run(self):
        price = self.data['close']
        ma91 = self.data['ma91']
        dc10up = self.data['dc10up']
        dc10dn = self.data['dc10dn']
        dc20up = self.data['dc20up']
        dc20dn = self.data['dc20dn']
        atr = self.data['atr']
        unit = self.get_unit(self.account['margin_balance'], price, atr, self.mianzhi)
        command=self.get_command()
        if command=='buy':
            self.trade(price, 0, 'open', 'buy', command)
        if command=='duichong':
            self.trade(price,round(self.account['margin_balance']*price/self.mianzhi,0),'open','chong',command)
        elif command=='openduo':
            self.trade(price,unit, 'open', 'buy',command)
        elif command=='addduo':
            self.trade(price, unit, 'open', 'buy',command)
        elif command=='zhiyingduo':
            self.trade(price, 0, 'close', 'sell',command='止盈多头')
        elif command=='zhisunduo':
            self.trade(price, 0, 'close', 'sell',command='止损多头')
        elif command=='openkong':
            self.trade(price, unit, 'open', 'sell',command)
        elif command=='addkong':
            self.trade(price, unit, 'open', 'sell',command)
        elif command=='zhiyingkong':
            self.trade(price, 0, 'close', 'buy',command='止盈空头')
        elif command=='zhisunkong':
            self.trade(price, 0, 'close', 'buy',command='止损空头')
        else:
            return
        #更新账户权益
        #
    def ready(self,coinname):
        self.coinname=coinname
        self.file_remove(self.coinname+'.txt')
        self.reason=''
        if coinname=='btc':
            self.mianzhi=100
        else:
            self.mianzhi=10
        self.data={
            'date':'',
            'timechuo':0,
            'open':0,
            'high':0,
            'low':0,
            'close':0,
            'ddate':'',
            'dvol':0,
            'ma91':0,
            'dc20up':0,
            'dc20dn':0,
            'dc10up':0,
            'dc10dn':0,
            'atr':0,
        }
        self.account={
            'usdt':10000,
            'margin_balance':0,
            'risk_rate':99999,
            'liquidation_price':99999,
            'volume_duo':0,
            'volume_kong':0,
            'volume_chong':0,
            'priceaver_duo': 0,
            'priceaver_kong': 0,
            'priceaver_chong': 0,
            'priceopen_last': 0,
            'times_open': 0,
        }
        self.trade_list=[]
        self.log_list=[]
        #删除txtcsv文件
        if os.path.exists("log.txt")==True:
            os.remove('log.txt')
        if os.path.exists("log.csv")==True:
            os.remove('log.csv')
        self.log('初始化完成')
    def start(self,coinname,date_start,date_end):
        self.ready(coinname)
        #读取历史数据
        df_1m = pd.read_csv(os.path.abspath('.') + '\\klineok\\' + coinname + '1m1dok.csv', index_col=0)
        df_1m =df_1m.reset_index()
        for i in range(len(df_1m)):
            self.data={
                'date':df_1m.loc[i, 'date'],
                'timechuo':int(df_1m.loc[i, 'timechuo']),
                'open':float(df_1m.loc[i, 'open']),
                'high':float(df_1m.loc[i, 'high']),
                'low':float(df_1m.loc[i, 'low']),
                'close':float(df_1m.loc[i, 'close']),
                'ddate':df_1m.loc[i, 'ddate'],
                'dvol':float(df_1m.loc[i, 'dvol']),
                'ma91':float(df_1m.loc[i, 'ma91']),
                'dc20up':float(df_1m.loc[i, 'dc20up']),
                'dc20dn':float(df_1m.loc[i, 'dc20dn']),
                'dc10up':float(df_1m.loc[i, 'dc10up']),
                'dc10dn':float(df_1m.loc[i, 'dc10dn']),
                'atr':float(df_1m.loc[i, 'atr']),
            }
            if self.data['timechuo']>self.date_totimechuo(date_start) and self.data['timechuo']<self.date_totimechuo(date_end):
                self.run()
        self.zongjie()

