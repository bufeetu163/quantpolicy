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
#注释完毕
class Policymodel():

    def timechuo_todate(self, timechuo):
        date = time.strftime("%Y-%m-%d_%H-%M", time.localtime(int(timechuo)))
        return date
    def date_totimechuo(self, date='2018-09-15'):
        timeStamp = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
        return timeStamp
    def get_date_now(self):
        res=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return res

    def get_timechuo_lingdian(self):
        zeroPoint = int(time.time()) - int(time.time() - time.timezone) % 86400
        return zeroPoint
    def get_jingdu(self,coinname):
        coinname=str(coinname).lower()
        if coinname=='btc':
            return 2
        elif coinname=='xrp':
            return 4
        elif coinname=='trx':
            return 5
        else:
            return 3
    def get_mianzhi(self,coinname):
        if str(coinname).lower()=='btc':
            return 100
        else:
            return 10
    def get_unsettled(self, price_aver, price, zhangshu, mianzhi, isduo):
        if zhangshu == 0 or price_aver == 0:
            return 0
        unsettled = round((1 / price_aver - 1 / price) * zhangshu * mianzhi, 4)
        fee_open = round(int(zhangshu) * mianzhi / price_aver * 0.03 * 0.01, 8)  # 开仓手续费
        fee_close = round(int(zhangshu) * mianzhi / price * 0.03 * 0.01, 8)  # 平仓手续费
        fee_close=0
        fee_open=0
        if isduo == True:
            return round(unsettled - fee_open - fee_close, 8)
        else:
            return round(0 - unsettled - fee_open - fee_close, 8)
    def get_fee(self, price, zhangshu, mianzhi):
        if zhangshu == 0 or price == 0:
            return 0
        fee = round(int(zhangshu) * mianzhi / price * 0.03 * 0.01, 8)  # 开仓手续费
        return fee
    def get_direction_maup(self, maup, madn, price, ma):
        rate_ma = (price - ma) / ma * 100
        if rate_ma<madn:
            return 'sleep'
        elif rate_ma<0:
            return 'kong'
        elif rate_ma<maup:
            return 'duo'
        else:
            return 'sleep'
    def get_direction_hekuan(self,price, ma):
        rate_ma = (price - ma) / ma * 100
        if rate_ma<0:
            return 'kong'
        else:
            return 'duo'
    def get_direction_qushi(self,price, ma,list_ma=[]):
        rate_ma = (price - ma) / ma * 100
        if rate_ma<0:
            res= 'kong'
        else:
            res= 'duo'
        if len(list_ma)<10:
            return 'sleep'
        else:
            if res=='duo' and list_ma[-1]<list_ma[-9]:
                self.log('本来是多,改成休眠')

                res='sleep'
            if res=='kong' and list_ma[-1]>list_ma[-9]:
                self.log('本来是空,改成休眠')
                res='sleep'
        return res
    def wg_show(self, list_wg=[]):
        if len(list_wg) == 0:
            self.log('网格为空')
            return
        for i in range(len(list_wg)):
            m = str(list_wg[i])
            # self.log(m)
            if list_wg[i]['status'] != 'duo_wait' and list_wg[i]['status'] != 'kong_wait':
                self.log(m)
    def chart_1(self, title, list1=[]):
        # 横坐标
        listx = []
        for i in range(len(list1)):
            listx.append(i + 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        liney1 = plt.plot(listx, list1)
        plt.setp(liney1, color='r')
        plt.title(title)
        plt.savefig(os.getcwd() + '/' + title + '.png')
        plt.close()
    def chart_2(self, title, list1=[], list2=[]):
        # 横坐标
        listx = []
        for i in range(len(list1)):
            listx.append(i + 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        liney1 = plt.plot(listx, list1)
        plt.setp(liney1, color='r')
        liney2 = plt.plot(listx, list2)
        plt.setp(liney2, color='g')
        plt.title(title)
        plt.savefig(os.getcwd() + '/' + title + '.png')
        plt.close()
    def chart_3(self, title, list1=[], list2=[], list3=[]):
        # 横坐标
        listx = []
        for i in range(len(list1)):
            listx.append(i + 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        liney1 = plt.plot(listx, list1)
        plt.setp(liney1, color='r')
        liney2 = plt.plot(listx, list2)
        plt.setp(liney2, color='g')
        liney3 = plt.plot(listx, list3)
        plt.setp(liney3, color='#8B008B')
        plt.title(title)
        plt.savefig(os.getcwd() + '/' + title + '.png')
        plt.close()
    def chart_4(self, title, list1=[], list2=[], list3=[], list4=[]):
        # 横坐标
        listx = []
        for i in range(len(list1)):
            listx.append(i + 1)
        plt.rcParams['font.sans-serif'] = ['SimHei']
        liney1 = plt.plot(listx, list1)
        plt.setp(liney1, color='r')
        liney2 = plt.plot(listx, list2)  # 多头绿色
        plt.setp(liney2, color='g')#绿色
        liney3 = plt.plot(listx, list3)
        plt.setp(liney3, color='#FFD700')  # 空头黄
        liney4 = plt.plot(listx, list4)
        plt.setp(liney4, color='#B8860B')  # 休眠棕色
        plt.title(title)
        plt.savefig(os.getcwd() + '/' + title + '.png')
        plt.close()
    def get_rate_margin(self, price, zhangshu, quanyi, mianzhi):
        # 持仓担保资产 = (合约面值 * 持仓合约数量) / 最新成交价 / 倍数；
        # 担保资产率 = (账户权益 / 占用担保资产) * 100 % – 调整系数
        if zhangshu == 0:
            return 99999
        else:
            margin = (mianzhi * zhangshu) / price / 10
            return round(quanyi / margin * 100 - 12, 2)
    def get_nianhua(self, rate_shouyi,time_start, timechuo_end):
        day = (int(timechuo_end) - int(time_start)) / 86400
        nianhua = float(rate_shouyi) * 365 / day
        return round(nianhua, 2)
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
    def get_num_lianxuyingkui(self,list_rate_shouyi_close={}):
        max_num_ying=0
        max_num_kui=0
        num_ying = 0
        num_kui = 0
        for shouyi in list_rate_shouyi_close:
            if shouyi > 0:
                num_ying += 1
                num_kui=0
                max_num_ying=max(max_num_ying,num_ying)
            else:
                num_kui += 1
                num_ying=0
                max_num_kui=max(max_num_kui,num_kui)
        return [max_num_ying,max_num_kui]
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
