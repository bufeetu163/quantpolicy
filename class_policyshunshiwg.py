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
from class_model import Model
#注释完毕


class Policyshunshiwg(Model):
    def __init__(self):
        self.dict_param={}
        self.dict_record={}
        self.dict_acc={}
        self.dict_data={}
        self.list_ma91=[]
    def zongjie(self,quanyi,price,money,fee_sum,date_start,date_end,huiche_max):
        # 资产 净利润 手续费  年化率 最大回撤 胜率 盈亏比
        # 持仓率 最低保证金率 连续盈利 连续亏损  结单次数 平均每次结单收益
        # 张数 间隔 止盈 止损
        fund=str(round(quanyi*price,2))
        rate_nianhua = str(self.get_nianhua(self.dict_record['list_rate_shouyi_fund'][-1], self.date_totimechuo(date_start), self.date_totimechuo(date_end)))
        res = self.get_shenglv_yingkui(self.dict_record['list_rate_shouyi_close'])
        rate_shenglv=str(res[0])
        rate_yingkui = str(res[1])
        rate_chicang=str(max(self.dict_record['list_rate_chicang']))
        rate_margin_min=str(min(self.dict_record['list_rate_margin']))
        times_shouyi=str(len(self.dict_record['list_rate_shouyi_close']))
        aver_shouyi=str(round(sum(self.dict_record['list_rate_shouyi_close'])/len(self.dict_record['list_rate_shouyi_close']),2))
        m1=self.coinname+'|'+str(fund)+'|'+str(money)+'|'+str(fee_sum)+'|'+str(rate_nianhua)+'|'+str(huiche_max)+'|'+str(rate_shenglv)+'|'+str(rate_yingkui)
        m2='|'+str(rate_chicang)+'|'+str(rate_margin_min)+'|'+str(times_shouyi)+'|'+str(aver_shouyi)
        m3=str(self.dict_param)
        self.txt_write('zongjie',m1+m2+m3)
        self.chart(self.coinname+'年化'+str(rate_nianhua)+'回撤'+str(huiche_max) + '胜率' + str(rate_shenglv) + '盈亏比' + str(rate_yingkui), self.dict_record['list_rate_jizhun'], self.dict_record['list_rate_shouyi_fund'])
        m1 = self.coinname + '|fund' + str(fund) + '|money' + str(money) + '|fee_sum' + str(fee_sum) + '|nianhua' + str(
            rate_nianhua) + '|最大回撤' + str(huiche_max) + '|胜率' + str(rate_shenglv) + '|盈亏比' + str(rate_yingkui)
        m2 = '|最大持仓率' + str(rate_chicang) + '|最低保证金率' + str(rate_margin_min) + '|平仓次数' + str(times_shouyi) + '|预期收益' + str(aver_shouyi)
        self.log(m1)
        self.log(m2)
    def log(self,content):
        self.txt_write(self.coinname,self.dict_data['date']+'----'+str(self.dict_data['close'])+'----'+content)
    def sell(self,quanyi,price,fund_start):
        coin= quanyi - (fund_start / price)
        money = coin* price * 0.998
        res={
            'coin':coin,
            'money':money,
        }
        return res
    def close(self,price,mianzhi,direction,timechuo,atr):
        lun_direction=self.dict_acc['lun_direction']
        lun_price_start=self.dict_acc['lun_price_start']
        lun_zhangshu_sum=self.dict_acc['lun_zhangshu_sum']
        lun_rate_shouyi_max=self.dict_acc['lun_rate_shouyi_max']
        lun_rate_shouyi=self.dict_acc['lun_rate_shouyi']
        zhiying=self.dict_param['zhiying']
        huiche=self.dict_param['huiche']
        zhisun_atr=self.dict_param['zhisun_atr']
        todo=''
        if lun_rate_shouyi_max>zhiying and lun_rate_shouyi<=lun_rate_shouyi_max*(1-huiche/100):
            if lun_direction == 'kong':
                todo = '止盈空'
            elif lun_direction=='duo':
                todo = '止盈多'
        if lun_direction == 'kong' and price>lun_price_start+zhisun_atr*atr:
            todo = '逆势止损空'
        elif lun_direction == 'duo' and price<lun_price_start-zhisun_atr*atr:
            todo = '逆势止损多'
        elif lun_direction == 'kong' and lun_rate_shouyi<-3:
            todo = '止损空'
        elif lun_direction == 'duo' and lun_rate_shouyi<-3:
            todo = '止损多'
        elif lun_direction=='sleep' and direction!='sleep':
            todo = '解冻'
        if todo == '止盈空' or todo == '止盈多' or todo == '止损空' or todo == '止损多' or todo == '解冻':
            #快照网格
            if todo!='解冻':
                self.wg_tocsv(self.coinname + todo, timechuo, price, lun_rate_shouyi, self.list_wg)
            #清空网格
            self.list_wg.clear()
            #记录平仓收益率
            if abs(lun_rate_shouyi)>1:
                self.dict_record['list_rate_shouyi_close'].append(lun_rate_shouyi)
            #计算手续费
            fee_close = self.get_fee(price, lun_zhangshu_sum, mianzhi)
            self.log('整体' + todo + ',收益率' + str(lun_rate_shouyi) + '手续费' + str(fee_close))
            return fee_close
        else:
            return False
    def uprecord(self,price,mianzhi,quanyi,money,fund_start,quanyi_start,price_start,lun_zhangshu_sum):
        fund=price*quanyi
        #资金收益率
        rate_shouyi_fund = round((fund+money) / fund_start * 100 - 100, 2)
        self.dict_record['list_rate_shouyi_fund'].append(rate_shouyi_fund)
        #币数收益率
        rate_shouyi_coin = round((fund + money) / price / quanyi_start * 100 - 100, 2)
        self.dict_record['list_rate_shouyi_coin'].append(rate_shouyi_coin)
        #K线基准率
        rate_jizhun = round(price / price_start * 100 - 100, 2)
        self.dict_record['list_rate_jizhun'].append(rate_jizhun)
        #保证金率
        rate_margin = self.get_rate_margin(price, lun_zhangshu_sum, quanyi, mianzhi)
        self.dict_record['list_rate_margin'].append(rate_margin)
        #持仓率
        rate_chicang = round(lun_zhangshu_sum / (fund / mianzhi), 2)
        self.dict_record['list_rate_chicang'].append(rate_chicang)
        #回撤率
        rate_huiche = round((10000 - fund) / (10000) * 100, 2)
        self.dict_record['list_rate_huiche'].append(rate_huiche)
        m1='==========方向'+str(self.dict_acc['lun_direction'])+'张数'+str(self.dict_acc['lun_zhangshu_sum'])+ '保证金率' + str(rate_margin)+ '持仓率' + str(rate_chicang)
        m2 = '==========权益' + str(self.dict_acc['quanyi']) + '资产' + str(fund) + '利润' + str(self.dict_acc['money']) + '手续费' + str(self.dict_record['fee_sum'])+'收益率' + str(rate_shouyi_fund) + '基准率' + str(rate_jizhun)
        m3 = '==========最低保证金率' + str(min(self.dict_record['list_rate_margin'])) + '最大持仓率' + str(max(self.dict_record['list_rate_chicang'])) + '最大回撤' + str(max(self.dict_record['list_rate_huiche']))
        self.log(m1)
        self.log(m2)
        self.log(m3)
    def ok(self,price,mianzhi):
        #遍历网格,更新单个收益,累计总收益,更新权益
        shouyi_sum = 0
        zhangshu_sum=0
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            price_wg = wg['price_wg']
            zhangshu_wg = wg['zhangshu_wg']
            status = wg['status']
            if status == 'duo_ok' or status == 'kong_ok' or status == 'chong_ok':
                if status == 'duo_ok':
                    shouyi= self.get_unsettled(price_wg, price, zhangshu_wg, mianzhi, True)
                    rate_shouyi = price / price_wg * 100 - 100
                else:
                    shouyi= self.get_unsettled(price_wg, price, zhangshu_wg, mianzhi, False)
                    rate_shouyi = 0-(price / price_wg * 100 - 100)
                self.list_wg[i]['shouyi'] = round(shouyi,2)
                self.list_wg[i]['rate_shouyi'] = round(rate_shouyi,2)
                self.list_wg[i]['rate_shouyi_max'] = max(self.list_wg[i]['rate_shouyi_max'],rate_shouyi)
                shouyi_sum += shouyi
                zhangshu_sum += zhangshu_wg

        res={
            'shouyi_sum':shouyi_sum,
            'zhangshu_sum':zhangshu_sum,
        }
        return res
    def ing(self,high,low):
        # 遍历网格,如果duo_ing  价格跌破就成交   waitkong 涨破就成交
        istradeok=False
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status'] == 'duo_ing' and low < wg['price_wg']:
                self.list_wg[i]['status'] = 'duo_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开多成功,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
                istradeok = True
            elif wg['status'] == 'kong_ing' and high > wg['price_wg']:
                self.list_wg[i]['status'] = 'kong_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开空成功,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
                istradeok = True
        return istradeok
    def wait(self,high,low):
        #遍历网格,如果waitduo  价格超过,就委托   waitkong 跌破就委托
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status']=='duo_wait' and high>wg['price_wg']:
                self.list_wg[i]['status']='duo_ing'
                # self.log('委托开多,委托价'+str(wg['price_wg'])+'委托张数'+str(wg['zhangshu_wg']))
            if wg['status']=='kong_wait' and low<wg['price_wg']:
                self.list_wg[i]['status'] = 'kong_ing'
                # self.log('委托开空,委托价'+str(wg['price_wg'])+'委托张数'+str(wg['zhangshu_wg']))
        return
    #创建网格
    def creat(self,price,quanyi,atr,mianzhi,direction):
        #准备参数
        self.list_wg = []
        zhangshu_chong=int(price*quanyi/mianzhi)
        zhangshu_base = max(int(self.dict_param['zhangshu_base']*zhangshu_chong),1)
        jiange_wg = round(atr * self.dict_param['jiange_atr'],2)
        status = ''
        zhangshu_wg=0
        geshu = 20
        for i in range(geshu * 2 + 1):
            id = i + 1
            price_wg = price + (geshu - i) * jiange_wg
            if direction == 'duo':
                status='duo_wait'
                if price_wg>price:
                    zhangshu_wg=zhangshu_base*2
                else:
                    zhangshu_wg=zhangshu_base
            elif direction == 'kong':
                status = 'kong_wait'
                if price_wg<price:
                    zhangshu_wg=zhangshu_base*2
                else:
                    zhangshu_wg=zhangshu_base
            dict_wg = {
                'id': id,
                'price_wg': round(price_wg, 3),
                'zhangshu_wg': zhangshu_wg,
                'status': status,
                'shouyi': 0,
                'rate_shouyi': 0,
                'rate_shouyi_max': 0,
                'date': self.dict_data['date'],
            }
            #加入列表
            if i == geshu:
                dict_wg['zhangshu_wg'] = zhangshu_chong
                dict_wg['status'] = 'chong_ok'
            if (direction!='sleep' or i==geshu) and price_wg>0:
                self.list_wg.append(dict_wg)
        self.dict_acc['lun_direction'] = direction
        self.dict_acc['lun_price_start'] = price
        self.dict_acc['lun_quanyi_start'] = quanyi
        self.dict_acc['lun_fund_start'] = quanyi * price
        self.dict_acc['lun_rate_shouyi'] = 0
        self.dict_acc['lun_rate_shouyi_max'] = 0
        self.dict_acc['lun_zhangshu_sum'] = zhangshu_chong
        self.log('账户='+str(self.dict_acc))
        self.log('创建网格完成,总格数'+str(len(self.list_wg))+'间隔'+str(jiange_wg)+'方向'+str(direction)+'初始资产'+str(quanyi*price))
    def buy(self,price):
        quanyi = round(self.dict_acc['money'] / price, 8)
        self.dict_acc['quanyi'] = quanyi
        self.dict_acc['money'] = 0
        self.dict_record['price_start'] = price
        self.dict_record['quanyi_start'] = quanyi
        self.dict_record['fund_start'] =price*quanyi
        self.log('系统:购买成功.得到权益' + str(quanyi)+'初始价格'+str(self.dict_record['price_start'])+'初始权益'+str(self.dict_record['quanyi_start']))
    #调用交易函数 买入 创建 开仓 止盈止损  记录 手续费 卖币
    def run(self,open,high,low,close,atr,ma,timechuo,mianzhi,direction):
        if self.dict_acc['quanyi'] == 0:
            self.buy(close)
            return
        else:
            if self.list_wg==[]:
                self.creat(close,self.dict_acc['quanyi'],atr,mianzhi,self.dict_data['direction'])
                self.txt_remove('创建网格成功')
            else:
                #1处理等待中的网格
                if len(self.list_wg)>1:
                    self.ing(high,low)
                    self.wait(high,low)
                #2处理已成交订单,更新权益 本轮张数
                res=self.ok(close,mianzhi)
                self.dict_acc['quanyi'] = round(self.dict_acc['lun_quanyi_start'] + res['shouyi_sum'], 8)
                self.dict_acc['lun_zhangshu_sum'] = res['zhangshu_sum']
                #3更新本轮收益率
                fund = round(close * self.dict_acc['quanyi'], 4)
                self.dict_acc['lun_rate_shouyi'] = round(fund / self.dict_acc['lun_fund_start'] * 100 - 100, 2)
                if self.dict_acc['lun_rate_shouyi'] > self.dict_acc['lun_rate_shouyi_max']:
                    self.dict_acc['lun_rate_shouyi_max'] = self.dict_acc['lun_rate_shouyi']
                    self.log('恭喜,本轮收益率达到' + str(self.dict_acc['lun_rate_shouyi']))
                #4记录数据
                if timechuo>self.dict_record['timechuo_record']:
                    self.dict_record['timechuo_record'] = timechuo + 3600 * 24
                    self.uprecord(close,
                                  mianzhi,
                                  self.dict_acc['quanyi'],
                                  self.dict_acc['money'],
                                  self.dict_record['fund_start'],
                                  self.dict_record['quanyi_start'],
                                  self.dict_record['price_start'],
                                  self.dict_acc['lun_zhangshu_sum'])
                #5止盈止损
                res=self.close(close,mianzhi,direction,timechuo,atr)
                #止盈止损成功后,扣除手续费
                if res!=False and res>0:
                    fee_close=res
                    self.log('扣手续费之前权益' + str(self.dict_acc['quanyi']))
                    self.dict_acc['quanyi'] -= 2 * fee_close
                    self.dict_record['fee_sum'] += 2 * fee_close
                    self.log('扣手续费之后权益' + str(self.dict_acc['quanyi']))
                    #止盈止损成功后,判断卖币
                    if self.dict_acc['quanyi'] * close- self.dict_record['fund_start']>50:
                        res=self.sell(self.dict_acc['quanyi'],close,self.dict_record['fund_start'])
                        self.dict_acc['quanyi'] -= res['coin']
                        self.dict_acc['money'] +=res['money']
                        self.log('卖币成功,卖出数量' + str(res['coin']) + '得到钱' + str(res['money']))
                    self.log('                                                ')
                    self.log('                                                ')
                    self.log('                                                ')
                    self.log('                                                ')
    #初始化容器 遍历指定区间k线,调用run
    def start(self,coinname,date_start,date_end,param={}):
        self.coinname=str(coinname).lower()
        self.txt_remove(self.coinname + '.txt')
        # 1全局参数
        param['jingdu']=self.get_jingdu(coinname)
        param['mianzhi']=self.get_mianzhi(coinname)
        self.dict_param = param
        # 2记录容器
        self.dict_record = {
            'timechuo_record': 0,
            'price_start': 0,
            'quanyi_start': 0,
            'fund_start': 0,
            'fee_sum': 0,
            'list_rate_shouyi_coin': [],
            'list_rate_shouyi_fund': [],
            'list_rate_jizhun': [],
            'list_rate_chicang': [0],
            'list_rate_margin': [],
            'list_rate_huiche': [],
            'list_rate_shouyi_close': [],
        }
        #3.账户容器
        self.dict_acc = {
            'quanyi': 0,
            'money': 10000,
            'lun_direction':'',
            'lun_price_start': 0,
            'lun_quanyi_start': 0,
            'lun_fund_start': 0,
            'lun_rate_shouyi': 0,
            'lun_rate_shouyi_max': 0,
            'lun_zhangshu_sum': 0,
        }
        # 4.数据容器
        self.dict_data = {
            'date': 0,
            'timechuo': 0,
            'open': 0,
            'high': 0,
            'low': 0,
            'close': 0,
            'ma': 0,
            'atr': 0,
        }
        self.list_wg = []
        print('初始化完成')
        # 遍历数据
        # 读取历史数据
        df_1m = pd.read_csv(os.path.abspath('.') + '\\klineok\\' + coinname + '1m1dok.csv', index_col=0).reset_index()
        for i in range(len(df_1m)):
            date= df_1m.loc[i, 'date']
            timechuo= int(df_1m.loc[i, 'timechuo'])
            open= float(df_1m.loc[i, 'open'])
            high= float(df_1m.loc[i, 'high'])
            low= float(df_1m.loc[i, 'low'])
            close= float(df_1m.loc[i, 'close'])
            ddate= df_1m.loc[i, 'ddate']
            dvol= float(df_1m.loc[i, 'dvol'])
            ma91= float(df_1m.loc[i, 'ma91'])
            dc20up= float(df_1m.loc[i, 'dc20up'])
            dc20dn= float(df_1m.loc[i, 'dc20dn'])
            dc10up= float(df_1m.loc[i, 'dc10up'])
            dc10dn= float(df_1m.loc[i, 'dc10dn'])
            atr= float(df_1m.loc[i, 'atr'])
            self.list_ma91.append(ma91)
            self.dict_data = {
                'date': date,
                'timechuo': timechuo,
                'open': open,
                'high': high,
                'low': low,
                'close': close,
                'ddate': ddate,
                'dvol': dvol,
                'ma91': ma91,
                'dc20up': dc20up,
                'dc20dn': dc20dn,
                'dc10up': dc10up,
                'dc10dn': dc10dn,
                'atr': atr,
                'direction':self.get_direction(close,ma91,dc20up,dc20dn,self.list_ma91)
            }
            if self.dict_data['timechuo'] > self.date_totimechuo(date_start) and self.dict_data[
                'timechuo'] < self.date_totimechuo(date_end) and self.dict_data['direction']!=False:
                self.run(open,high,low,close,atr,ma91,timechuo,self.dict_param['mianzhi'],self.dict_data['direction'])
            elif self.dict_data['timechuo'] > self.date_totimechuo(date_end):
                break
        self.zongjie(quanyi=self.dict_acc['quanyi'],
                     price=self.dict_data['close'],
                     money=self.dict_acc['money'],
                     fee_sum=self.dict_record['fee_sum'],
                     date_start=date_start,
                     date_end=date_end,
                     huiche_max=max(self.dict_record['list_rate_huiche']))



