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
        pass
    def get_direction(self,price,ma):
        if price>ma:
            return 'duo'
        else:
            return 'kong'
    def get_zhangshu(self,isduo=True):
        zhangshu_duo = 0
        zhangshu_kong = 0
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status'] == 'kong_ok':
                zhangshu_kong += wg['zhangshu_wg']
            if wg['status'] == 'duo_ok':
                zhangshu_duo += wg['zhangshu_wg']
        if isduo==True:
            return zhangshu_duo
        else:
            return zhangshu_kong
    def log_paramlist(self,content):
        content = str(content)+ '\n'
        url=os.getcwd() + '/logparamlist.txt'
        f = open(url, mode='a+')
        f.write(str(content))
        # f.write(str(content)+'        '+str(self.get_date_now()))
        f.close()
        print(content)
    def zongjie(self):
        # 资产 净利润 手续费  年化率 最大回撤 胜率 盈亏比
        # 持仓率 最低保证金率 连续盈利 连续亏损  结单次数 平均每次结单收益
        # 张数 间隔 止盈 止损
        fund=str(round(float(self.dict_acc['quanyi'])*float(self.dict_data['close']),2))
        money=str(self.dict_acc['money'])
        fee=str(self.dict_record['fee_sum'])
        rate_nianhua = str(self.get_nianhua(self.dict_record['list_rate_shouyi_fund'][-1], self.date_totimechuo('2018-09-15'), self.dict_param['timechuo_end']))
        huiche_max=str(max(self.dict_record['list_rate_huiche']))
        res = self.get_shenglv_yingkui(self.dict_record['list_rate_shouyi_close'])
        rate_shenglv=str(res[0])
        rate_yingkui = str(res[1])
        rate_chicang=str(max(self.dict_record['list_rate_chicang']))
        rate_margin_min=str(min(self.dict_record['list_rate_margin']))
        res=self.get_num_lianxuyingkui(self.dict_record['list_rate_shouyi_close'])
        num_lianxuying=str(res[0])
        num_lianxukui=str(res[1])
        num_shouyi=str(len(self.dict_record['list_rate_shouyi_close']))
        aver_shouyi=str(sum(self.dict_record['list_rate_shouyi_close'])/len(self.dict_record['list_rate_shouyi_close']))
        m1=self.coinname+'|'+fund+'|'+money+'|'+fee+'|'+rate_nianhua+'|'+huiche_max+'|'+rate_shenglv+'|'+rate_yingkui
        m2='|'+rate_chicang+'|'+rate_margin_min+'|'+num_lianxuying+'|'+num_lianxukui+'|'+num_shouyi+'|'+aver_shouyi
        m3='|' + str(self.dict_param['jiange']) + '|' + str(self.dict_param['zhangshu_shun'])+ '|' + str(self.dict_param['zhangshu_ni']) + '|' + str(self.dict_param['zhiying']) + '|' + str(self.dict_param['zhisun'])+ '|' + str(self.dict_param['sleep_day'])
        m3= '|' + str(self.dict_param['zhangshu_shun'])+ '|' + str(self.dict_param['zhiying']) + '|' + str(self.dict_param['zhisun'])+ '|' + str(self.dict_param['sleep_day'])
        self.log_paramlist(m1+m2+m3)
        self.log_paramlist(self.dict_record['list_rate_shouyi_close'])
        self.chart(self.coinname+'年化'+str(rate_nianhua)+'回撤'+str(max(self.dict_record['list_rate_huiche'])), self.dict_record['list_rate_jizhun'], self.dict_record['list_rate_shouyi_fund'])


    def wg_tocsv(self,title,timechuo,price):
        name = ['id', 'price_wg', 'zhangshu_wg','status','shouyi','rate_shouyi','rate_shouyi_max','timechuo','date']
        test = pd.DataFrame(columns=name, data=self.list_wg)  # 数据有三列，列名分别为one,two,three
        datem = self.timechuo_todate(timechuo)
        zhangshu_duo = self.get_zhangshu(True)
        zhangshu_kong = self.get_zhangshu(False)
        m = '价格' + str(price) + '回撤' + str(max(self.dict_record['list_rate_huiche'])) + 'duo' + str(zhangshu_duo) + 'kong' + str(zhangshu_kong) + '本轮收益率' + str(self.dict_acc['lun_rate_shouyi'])
        test.to_csv(os.getcwd() + '/' + datem + m + title + '.csv', encoding='gbk')

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
    def close(self,price,mianzhi,zhiying,huiche,zhisun,zhisun_atr,lun_direction,lun_rate_shouyi,lun_rate_shouyi_max,lun_zhangshu_sum,timechuo):
        todo=''
        if lun_rate_shouyi_max>zhiying and lun_rate_shouyi<=lun_rate_shouyi_max*(1-huiche*0.01):
            todo = '止盈'
        if lun_rate_shouyi<0-abs(zhisun):
            if lun_direction == 'kong':
                todo = '止损空'
            elif lun_direction=='duo':
                todo = '止损多'
            else:
                todo = '止损其他'
                exit()
        if todo == '止盈' or todo == '止损空' or todo == '止损多' or todo == '解冻':
            #快照网格
            self.wg_tocsv(self.coinname+todo,timechuo,price)
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
        m1='本轮方向'+str(self.dict_acc['lun_direction'])+'张数'+str(self.dict_acc['lun_zhangshu_sum'])+ '保证金率' + str(rate_jizhun)+ '持仓率' + str(rate_chicang)
        m2 = '当前权益' + str(self.dict_acc['quanyi']) + '资产' + str(fund) + '净利润' + str(self.dict_acc['money']) + '手续费' + str(self.dict_record['fee_sum'])+'收益率' + str(rate_shouyi_fund) + '基准率' + str(rate_jizhun)
        m3 = '累计最低保证金率' + str(min(self.dict_record['list_rate_margin'])) + '最大持仓率' + str(max(self.dict_record['list_rate_chicang'])) + '最大回撤' + str(max(self.dict_record['list_rate_huiche']))
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
        for i in range(len(self.list_wg)):
            wg = self.list_wg[i]
            if wg['status'] == 'duo_ing' and low < wg['price_wg']:
                self.list_wg[i]['status'] = 'duo_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开多成交,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
            elif wg['status'] == 'kong_ing' and high > wg['price_wg']:
                self.list_wg[i]['status'] = 'kong_ok'
                self.list_wg[i]['date'] = self.dict_data['date']
                self.log('开空成交,成交价' + str(wg['price_wg']) + '成交张数' + str(wg['zhangshu_wg']))
        return
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
    def creat(self,price,atr,ma,mianzhi,fund,param_zhangshu_ni,param_jiange):
        self.list_wg = []
        zhangshu_chong=int(fund/mianzhi)
        zhangshu_ni = max(round(param_zhangshu_ni*zhangshu_chong,2),1)
        zhangshu_ni=int(zhangshu_ni)
        zhangshu_shun=zhangshu_ni*2
        jiange_wg = round(atr * param_jiange,2)
        direction=self.get_direction(price,ma)
        status = ''
        zhangshu_wg=0
        geshu = 20
        for i in range(geshu * 2 + 1):
            id = i + 1
            price_wg = price + (geshu - i) * jiange_wg
            if direction == 'duo':
                status='duo_wait'
                if price_wg>price:
                    zhangshu_wg=zhangshu_shun
                else:
                    zhangshu_wg=zhangshu_ni
            elif direction == 'kong':
                status = 'kong_wait'
                if price_wg<price:
                    zhangshu_wg=zhangshu_shun
                else:
                    zhangshu_wg=zhangshu_ni
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
        self.dict_acc['lun_quanyi_start'] = self.dict_acc['quanyi']
        self.dict_acc['lun_fund_start'] = self.dict_acc['quanyi'] * price
        self.dict_acc['lun_price_high']=price
        self.dict_acc['lun_price_low']=price
        self.dict_acc['lun_rate_shouyi'] = 0
        self.dict_acc['lun_rate_shouyi_max'] = 0
        self.dict_acc['lun_zhangshu_sum'] = zhangshu_chong
        self.log('账户='+str(self.dict_acc))
        self.log('创建网格完成,总格数'+str(len(self.list_wg))+'间隔'+str(jiange_wg)+'方向'+str(direction)+'初始资产'+str(fund))
    def buy(self,price):
        quanyi = round(self.dict_acc['money'] / price, 8)
        self.dict_acc['quanyi'] = quanyi
        self.dict_acc['money'] = 0
        self.dict_record['price_start'] = price
        self.dict_record['quanyi_start'] = quanyi
        self.dict_record['fund_start'] =price*quanyi
        self.log('系统:购买成功.得到权益' + str(quanyi)+'初始价格'+str(self.dict_record['price_start'])+'初始权益'+str(self.dict_record['quanyi_start']))
    def run(self,open,high,low,close,atr,ma,timechuo):
        if self.dict_acc['quanyi'] == 0:
            self.buy(close)
            return
        else:
            mianzhi = self.dict_param['mianzhi']
            if self.list_wg==[]:
                self.creat(close,atr,ma,mianzhi,self.dict_acc['quanyi']*close,self.dict_param['zhangshu_ni'],self.dict_param['jiange'])
                self.txt_remove('创建网格成功')
            else:
                self.dict_acc['lun_price_high'] = max(self.dict_acc['lun_price_high'], high)
                self.dict_acc['lun_price_low'] = min(self.dict_acc['lun_price_low'], low)
                if len(self.list_wg)>1:
                    self.ing(high,low)
                    self.wait(high,low)
                #处理已成交订单
                res=self.ok(close,mianzhi)
                self.dict_acc['quanyi'] = round(self.dict_acc['lun_quanyi_start'] + res['shouyi_sum'], 8)
                self.dict_acc['lun_zhangshu_sum'] = res['zhangshu_sum']
                #更新本轮收益率
                fund = round(close * self.dict_acc['quanyi'], 4)
                self.dict_acc['lun_rate_shouyi'] = round(fund / self.dict_acc['lun_fund_start'] * 100 - 100, 2)
                if self.dict_acc['lun_rate_shouyi'] > self.dict_acc['lun_rate_shouyi_max']:
                    self.dict_acc['lun_rate_shouyi_max'] = self.dict_acc['lun_rate_shouyi']
                    self.log('恭喜,本轮收益率达到' + str(self.dict_acc['lun_rate_shouyi']))
                #记录数据
                if timechuo>self.dict_record['timechuo_record']:
                    self.dict_record['timechuo_record'] = timechuo + 3600 * 4
                    self.uprecord(close,
                                  mianzhi,
                                  self.dict_acc['quanyi'],
                                  self.dict_acc['money'],
                                  self.dict_record['fund_start'],
                                  self.dict_record['quanyi_start'],
                                  self.dict_record['price_start'],
                                  self.dict_acc['lun_zhangshu_sum'])
                #止盈止损
                res=self.close(close,mianzhi,
                           self.dict_param['zhiying'],
                           self.dict_param['huiche'],
                           self.dict_param['zhisun'],
                           self.dict_param['zhisun_atr'],
                           self.dict_acc['lun_direction'],
                           self.dict_acc['lun_rate_shouyi'],
                           self.dict_acc['lun_rate_shouyi_max'],
                           self.dict_acc['lun_zhangshu_sum'],
                           timechuo
                           )
                #扣除手续费
                if res!=False and res>0:
                    fee_close=res
                    self.log('扣手续费之前权益' + str(self.dict_acc['quanyi']))
                    self.dict_acc['quanyi'] -= 2 * fee_close
                    self.dict_record['fee_sum'] += 2 * fee_close
                    self.log('扣手续费之后权益' + str(self.dict_acc['quanyi']))
                    #卖币
                    if self.dict_acc['quanyi'] * close- self.dict_record['fund_start']>50:
                        res=self.sell(self.dict_acc['quanyi'],close,self.dict_record['fund_start'])
                        self.dict_acc['quanyi'] += res['coin']
                        self.dict_acc['money'] +=res['money']
                        self.log('卖币成功,卖出数量' + str(res['coin']) + '得到钱' + str(res['money']))
    def start(self,coinname,date_start,date_end,param={}):
        self.coinname=str(coinname).lower()
        # 1参数容器
        self.dict_param=param
        self.dict_param['jingdu']=self.get_jingdu(coinname)
        self.dict_param['mianzhi']=self.get_mianzhi(coinname)
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
            'lun_price_high': 0,
            'lun_price_low': 0,
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
        self.txt_remove(self.coinname+'.txt')
        # 遍历数据
        # 读取历史数据
        df_1m = pd.read_csv(os.path.abspath('.') + '\\klineok\\' + coinname + '1m1dok.csv', index_col=0)
        df_1m = df_1m.reset_index()
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
            }
            if self.dict_data['timechuo'] > self.date_totimechuo(date_start) and self.dict_data[
                'timechuo'] < self.date_totimechuo(date_end):
                self.run(open,high,low,close,atr,ma91,timechuo)





