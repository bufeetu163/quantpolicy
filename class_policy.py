# @Time : 2020/2/14 23:20 
# @Author : bufeetu
# @File : class_model.py
import time, datetime
import os
import requests
import json
import pymysql
import time, datetime
import matplotlib.pyplot as plt
import os
import json
import pandas as pd
from class_base import Base
import numpy as np
#注释完毕
class Policy(Base):
    #获取精度
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
    #获取面值
    def get_mianzhi(self,coinname):
        if str(coinname).lower()=='btc':
            return 100
        else:
            return 10
    #计算未结算收益
    def get_unsettled(self, price_aver, price, zhangshu, mianzhi, isduo):
        if zhangshu == 0 or price_aver == 0:
            return 0
        unsettled = round((1 / price_aver - 1 / price) * zhangshu * mianzhi, 4)
        if isduo == True:
            return round(unsettled, 8)
        else:
            return round(0 - unsettled, 8)
    #计算手续费
    def get_fee(self, price, zhangshu, mianzhi):
        if zhangshu == 0 or price == 0:
            return 0
        fee = round(int(zhangshu) * mianzhi / price * 0.03 * 0.01, 8)  # 开仓手续费
        return fee
    #网格写出到csv文件
    def wg_tocsv(self,title,timechuo,price,lun_rate_shouyi,list_wg=[]):
        name = ['id', 'price_wg', 'zhangshu_wg','status','shouyi','rate_shouyi','rate_shouyi_max','date']
        df = pd.DataFrame(columns=name, data=list_wg)  # 数据有三列，列名分别为one,two,three
        datem = self.timechuo_todate(timechuo)
        m =title+ '收益率' + str(lun_rate_shouyi)+ '价格' + str(price)
        title=os.getcwd() + '\\'+str(timechuo)+ m+ '.csv'
        df.to_csv(title, encoding='gbk',index=None)
    #绘制数据图
    def chart(self, title, list1=[], list2=[], list3=[], list4=[]):
        # 横坐标
        listx = []
        for i in range(len(list1)):
            listx.append(i + 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        liney1 = plt.plot(listx, list1)
        plt.setp(liney1, color='r')
        if len(list2)>0:
            liney2 = plt.plot(listx, list2)  # 多头绿色
            plt.setp(liney2, color='g')  # 绿色
            if len(list3) > 0:
                liney3 = plt.plot(listx, list3)
                plt.setp(liney3, color='#FFD700')  # 空头黄
                if len(list4)>0:
                    liney4 = plt.plot(listx, list4)
                    plt.setp(liney4, color='#B8860B')  # 休眠棕色
        plt.title(title)
        plt.savefig(os.getcwd() + '/' + title + '.png')
        plt.close()
    #计算保证金率
    def get_rate_margin(self, price, zhangshu, quanyi, mianzhi):
        # 持仓担保资产 = (合约面值 * 持仓合约数量) / 最新成交价 / 倍数；
        # 担保资产率 = (账户权益 / 占用担保资产) * 100 % – 调整系数
        if zhangshu == 0:
            return 99999
        else:
            margin = (mianzhi * zhangshu) / price / 10
            rate_margin=round(quanyi / margin * 100 - 12, 2)
            return rate_margin
    #计算年化率
    def get_rate_nianhua(self, rate_shouyi,time_start, timechuo_end):
        day = (int(timechuo_end) - int(time_start)) / 86400
        nianhua = float(rate_shouyi) * 365 / day
        return round(nianhua, 2)
    #计算胜率和盈亏比
    def get_shenglv_yingkui(self,list_rate_shouyi_close={}):
        num_close = len(list_rate_shouyi_close)
        num_ying = 0
        num_kui = 0
        sum_ying = 0
        sum_kui = 0
        for shouyi in list_rate_shouyi_close:
            if shouyi > 0:
                num_ying += 1
                sum_ying += shouyi
            else:
                num_kui += 1
                sum_kui += shouyi
        if num_ying==0 or num_kui==0:
            return [0,0]
        shenglv=num_ying/num_close
        yingkui = (sum_ying / num_ying) / (sum_kui / num_kui)
        return [round(shenglv,2),round(abs(yingkui),2)]
    #计算最大回撤率
    def get_huiche_max(self, list_rate_shouyi=[]):
        length = len(list_rate_shouyi)
        huiche_max = 0
        rate_shouyi_max = 0
        if length == 0:
            return 0
        else:
            for i in range(length):
                rate_shouyi = list_rate_shouyi[i]
                #更新最大收益率
                rate_shouyi_max = max(rate_shouyi_max, rate_shouyi)
                #回撤部分除去(最大收益率+100)
                huiche = abs(rate_shouyi - rate_shouyi_max) / (100 + rate_shouyi_max)
                huiche_max = max(huiche_max, huiche)
        return round(huiche_max * 100, 4)
    #根据均线和ma获取趋势方向
    def get_direction_by_ma60_ma91(self,price,ma60,ma91):
        if price>ma60>ma91:#正在上涨
            return 'duo'
        elif ma60>price>ma91:#上涨回调
            return 'duo'
        elif ma60>ma91>price:#急速回调,不一定涨
            return 'sleep'
        elif ma91>ma60>price:#正在下跌
            return 'kong'
        elif ma91>price>ma60:#下跌回调,定继续跌
            return 'kong'
        elif price>ma91>ma60:#急速拉高,定继续跌
            return 'kong'
        else:
            return 'sleep'
