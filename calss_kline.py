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
class Kline(Base):
    def __init__(self):
        print('创建kline类')
    def kline_daytomin(self,coinname):
        df_1d = pd.read_csv(os.path.abspath('.') + '\\kline_1d\\' + coinname + '_1d.csv', index_col=0)
        df_1m = pd.read_csv(os.path.abspath('.') + '\\kline_1m\\' + coinname + '_1m.csv')
        df_1m.dropna(subset=['date'],inplace=True)
        df_1m['ddate']=None
        df_1m['dvol']=0
        df_1m['ma91']=0
        df_1m['dc20up']=0
        df_1m['dc20dn']=0
        df_1m['dc10up']=0
        df_1m['dc10dn']=0
        df_1m['atr']=0
        #遍历日线，修改日线的值
        for i in range(len(df_1d)):
            timechuo_1d = int(df_1d.loc[i, 'timechuo'])
            date_1d = df_1d.loc[i, 'date']
            print('日线'+date_1d)
            #找到对应的分钟线
            timechuo_start=timechuo_1d+86400
            timechuo_end=timechuo_1d+86400*2
            df_ls=df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end)]
            if len(df_ls)>0 and df_1d.loc[i, 'ma91']>0:
                # print('需要修改该列')
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('ddate')]=date_1d
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('dvol')]=df_1d.loc[i, 'vol']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('ma91')]=df_1d.loc[i, 'ma91']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('dc20up')]=df_1d.loc[i, 'dc20up']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('dc20dn')]=df_1d.loc[i, 'dc20dn']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('dc10up')]=df_1d.loc[i, 'dc10up']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('dc10dn')]=df_1d.loc[i, 'dc10dn']
                df_1m.loc[(df_1m['timechuo'] >= timechuo_start) & (df_1m['timechuo'] < timechuo_end),('atr')]=df_1d.loc[i, 'atr']
        path = os.path.abspath('.') +'\\'+ coinname + '1m1dok.csv'
        #清空没有日线数据
        df_1m.dropna(subset=['ddate'],inplace=True)
        print(path)
        df_1m.to_csv(path, encoding="utf-8")
    #日线:计算ma  dc atr
    def kline_atr(self,coinname,path):
        atr_0615={
            'btc':378.52,
            'eth':45.54,
            'eos':1.5553,
            'ltc':8.71,
            'etc':1.6945,
        }
        df = pd.read_csv(path, index_col=0)
        df['yclose'] = df['close'].shift(1)
        # 计算tr
        df['tr'] = 0
        for i in range(len(df)):
            df.loc[i, 'tr'] = max(abs(df.loc[i, 'high'] - df.loc[i, 'low']),
                                  abs(df.loc[i, 'high'] - df.loc[i, 'yclose']),
                                  abs(df.loc[i, 'yclose'] - df.loc[i, 'low']))
        # 计算atr
        df['atr'] = 0
        for i in range(len(df)):
            if i == 0:
                df.loc[i, 'atr'] = atr_0615[coinname]
            else:
                if coinname == 'etc' and df.loc[i, 'timechuo'] == self.date_totimechuo('2018-06-25 08:00'):
                    df.loc[i, 'atr'] = atr_0615[coinname]
                df.loc[i, 'atr'] = round((df.loc[i - 1, 'atr'] * 13 + df.loc[i, 'tr']) / 14, 4)
        df.to_csv(path, encoding="utf-8")
        print(path + '增加atr成功')
    def kline_dc(self,path):
        df = pd.read_csv(path, index_col=0)
        df['dc20up'] = 0
        df['dc20dn'] = 0
        df['dc10up'] = 0
        df['dc10dn'] = 0
        for i in range(len(df)):
            df.loc[i, 'dc20up'] = round(df.loc[i - 20:i, 'high'].max(), 4)
            df.loc[i, 'dc20dn'] = round(df.loc[i - 20:i, 'low'].min(), 4)
            df.loc[i, 'dc10up'] = round(df.loc[i - 10:i, 'high'].max(), 4)
            df.loc[i, 'dc10dn'] = round(df.loc[i - 10:i, 'low'].min(), 4)
        df.to_csv(path, encoding="utf-8")
        print(path + '增加dc成功')
    def kline_ma91(self,path):
        df = pd.read_csv(path)
        # 计算ma91
        df['ma91'] = 0
        for i in range(len(df)):
            date = df.loc[i, 'date']
            df.loc[i, 'ma91'] = round(df.loc[i - 90:i, 'close'].mean(), 4)
            if i < 91:
                df.loc[i, 'ma91'] = 0
        df.to_csv(path, encoding="utf-8")
        print(path + '增加ma91成功')
    #分钟线去重
    def kline_delrepeat(self,coinname,path):
        # path = os.path.abspath('.') + '\\kline\\' + coinname + '\\'
        df_1m = pd.read_csv(path)
        for i in range(len(df_1m)):
            # timechuo = df_1m.loc[i, 'timechuo']
            if i>1:
                if df_1m.loc[i, 'timechuo']<df_1m.loc[i-1, 'timechuo']+60:
                    self.txt_write('debuykline' + coinname, '出现重复,后者小于前者,' + df_1m.loc[i, 'date'])
                if df_1m.loc[i, 'timechuo']>df_1m.loc[i-1, 'timechuo']+60:
                    self.txt_write('debuykline'+coinname,'开始维护,'+df_1m.loc[i-1, 'date'])
                    self.txt_write('debuykline'+coinname,'结束维护,'+df_1m.loc[i, 'date'])
    #分钟线：合并
    def kline_merge(self,coinname):
        path = os.path.abspath('.') + '\\kline\\' + coinname + '\\'
        list_csv = os.listdir(path)
        for i in range(len(list_csv)):
            csv = list_csv[i]
            print('i=' + str(i) + '   ' + csv)
            if i == 0:
                df = pd.read_csv(path + csv, index_col=0)
            else:
                df = df.append(pd.read_csv(path + csv, index_col=0))
        df.drop_duplicates(keep='last', inplace=True)
        df.to_csv(coinname + '.csv', encoding="utf-8")
        print(coinname + '合并完成')
    #采集k线初始数据
    def kline_to_df(self, list_kline):
        # 加入date
        for i in range(len(list_kline)):
            list_kline[i][0] = int(list_kline[i][0] / 1000)
            date = self.timechuo_todate(list_kline[i][0])
            list_kline[i].append(date)
        # 创建df
        df = pd.DataFrame(list_kline)
        # 去掉不需要数据
        df.drop([6, 7, 8, 9, 10, 11], axis=1, inplace=True)
        # 设置列名
        df.columns = ['timechuo', 'open', 'high', 'low', 'close', 'vol', 'date']
        # 转换数据类型
        df['timechuo'] = df['timechuo'].astype(int)
        df['open'] = df['open'].astype(float)
        df['high'] = df['high'].astype(float)
        df['low'] = df['low'].astype(float)
        df['close'] = df['close'].astype(float)
        df['vol'] = df['vol'].astype(float)
        df['date'] = df['date'].astype(str)
        # 掉换列位置
        list_columns = ['date', 'timechuo', 'open', 'high', 'low', 'close', 'vol']
        df = df[list_columns]
        # 设置日期为索引
        df.set_index('date', inplace=True)
        return df
    def get_kline_csv(self,symbol='BTCUSDT',zhouqi='1m',timechuo_start=1528992000,limit=1000):
        while timechuo_start < time.time() - 86400:
            url = 'https://api.binance.com/api/v1/klines?symbol=' + symbol + '&interval=' + zhouqi + '&startTime=' + str(
                timechuo_start) + '000&limit=' + str(limit)
            list_kline = self.get_url(url)
            # list_kline=[[1528992000000,"6344.35000000","6363.70000000","6344.35000000","6360.50000000","85.01222100",1528992059999,"539923.71015506",237,"73.87742200","469218.13245320","0"],[1528992060000,"6360.49000000","6369.00000000","6358.02000000","6364.71000000","26.85137700",1528992119999,"170899.79208065",290,"14.51892300","92423.48531447","0"],[1528992120000,"6366.94000000","6372.89000000","6348.91000000","6354.98000000","65.19726800",1528992179999,"414719.49610261",289,"43.72353000","278114.00497471","0"],[1528992180000,"6362.43000000","6366.14000000","6351.21000000","6352.67000000","32.84084500",1528992239999,"208883.86023217",191,"13.13099100","83510.71989132","0"],[1528992240000,"6357.40000000","6363.66000000","6353.05000000","6361.00000000","24.05830600",1528992299999,"153013.93047432",115,"15.70252800","99867.19997429","0"],[1528992300000,"6361.00000000","6366.99000000","6355.56000000","6359.98000000","18.53329500",1528992359999,"117910.21401926",130,"11.29712200","71870.88532012","0"],[1528992360000,"6359.00000000","6375.60000000","6357.85000000","6370.00000000","39.18811200",1528992419999,"249481.41656465",206,"23.99206100","152721.29636031","0"],[1528992420000,"6370.01000000","6385.00000000","6360.00000000","6361.84000000","31.75946100",1528992479999,"202358.78430921",215,"16.18494800","103155.97920260","0"],[1528992480000,"6363.16000000","6369.85000000","6360.00000000","6364.07000000","23.63020100",1528992539999,"150373.48547074",98,"15.27386500","97203.10382152","0"],[1528992540000,"6366.58000000","6366.69000000","6360.02000000","6360.39000000","18.63935200",1528992599999,"118580.25908958",79,"7.79828300","49619.63391152","0"]]
            df = self.kline_to_df(list_kline)
            # 保存文件
            path = os.path.abspath('.') + '/' + zhouqi + '_' + str(symbol).lower()
            if not os.path.exists(path):
                os.mkdir(path)
                print('创建文件夹' + path)
            path = path + '/' + str(df.iloc[0, 0]) + ".csv"
            df.to_csv(path, encoding="utf-8")
            print(self.timechuo_todate(df.iloc[0, 0]) + ' 保存成功 ' + str(path))
            if zhouqi == '1m':
                timechuo_start = df.iloc[-1, 0] + 60
            elif zhouqi == '1d':
                timechuo_start = df.iloc[-1, 0] + 60 * 60 * 24
            else:
                print('周期不存在')
                exit()
            time.sleep(1)

