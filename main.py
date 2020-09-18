# coding=UTF-8
import time, datetime
import os
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from calss_kline import Kline
from class_base import Base
from class_policyshunshiwg import Policyshunshiwg
from calss_kline import Kline
import pdb
from HuobiDMService import HuobiDM
from class_policywgma60ma91 import Policywgma60ma91
def piliang_order():
    dm = HuobiDM('bb744223-32147a86-56597f7f-ez2xc4vb6n', '8bc9bf60-64d68dfc-2cc3f4f7-b08de')
    # dm.order_piliang(
    #     coinname='trx',
    #     price_start=0.043,
    #     jiange=0.00005,
    #     times=316,
    #     volume=1,
    #     direction='sell',
    #     offset='open',
    # )
    dm.order_piliang(
        coinname='eos',
        price_start=2.82,
        jiange=0.001,
        times=405,
        volume=1,
        direction='sell',
        offset='close',
        contract_type='next_quarter'
    )
    # dm.order_piliang(
    #     coinname='link',
    #     price_start=11.9,
    #     jiange=0.03,
    #     times=100,
    #     volume=1,
    #     direction='sell',
    #     offset='open',
    # )
    dm.order_piliang(
        coinname='btc',
        price_start=11223,
        jiange=10,
        times=100,
        volume=1,
        direction='sell',
        offset='close',
        contract_type='quarter'
    )
    # dm.order_piliang(
    #     coinname='btc',
    #     price_start=10750,
    #     jiange=10,
    #     times=47,
    #     volume=1,
    #     direction='sell',
    #     offset='close',
    # )


def mainjunxian():
    robot=Policywgma60ma91()
    param={
        'zhangshu':0.03,
        'jiange':0.1,#每格间距多少atr
        'zhiying':8,#止盈比例
        'huiche':20,#回撤比例
        'zhisun':1,#逆势多少atr
        'sleep':1,#休眠天数
    }
    time_start=time.time()
    robot.start(
        coinname='eth',
        date_start='2018-09-15 12:00',
        date_end='2018-12-15 12:00',
        param=param
    )
    time_cost=time.time()-time_start
    print('花费时间'+str(round(time_cost,2))+'秒')
def main_alljunxian():
    '''
    第一次遍历 2020年9月11日 08:42:20
    '''
    list_zhisun = [1, 2, 3]# 1北京2上海3香港
    list_zhisun = [3]
    list_zhangshu=[0.03,0.05,0.07,0.09]
    list_jiange=[0.1,0.3,0.5,0.7]
    list_zhiying=[8,11,5,2]
    list_sleep=[1,3,5,7]
    '''
        第2次遍历 2020年9月11日 08:42:20
    '''
    list_zhisun = [1,0.5]
    list_zhangshu = [0.03, 0.05, 0.07, 0.09]
    list_jiange = [0.1,0.5]
    list_zhiying = [8, 11,14] #北京8上海11香港14
    list_zhiying = [14] #北京8上海11香港14
    list_sleep = [3,7]
    i=0

    robot = Policywgma60ma91()
    for zhangshu in list_zhangshu:
        for jiange in list_jiange:
            for zhiying in list_zhiying:
                for zhisun in list_zhisun:
                    for sleep in list_sleep:
                        # 总数量 4*4*4*3*4=4*768  四台,每台768个,,,, 768/12=
                        param = {
                            'zhangshu': zhangshu,
                            'jiange': jiange,  # 每格间距多少atr
                            'zhiying': zhiying,  # 止盈比例
                            'huiche': 20,  # 回撤比例
                            'zhisun': zhisun,  # 逆势多少atr
                            'sleep': sleep,  # 休眠天数
                        }
                        robot.start(
                            coinname='eth',
                            date_start='2018-09-15 12:00',
                            date_end='2019-12-15 12:00',
                            param=param
                        )
                        i+=1
                        print('遍历完成'+str(i))
def main():
    pass
if __name__ == '__main__':
    # piliang_order()
    main()

