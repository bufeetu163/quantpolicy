import time, datetime
import os
import requests
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from calss_kline import Kline
from class_base import Base
from class_turtle import Turtle
from class_policyshunshiwg import Policyshunshiwg
from calss_kline import Kline
import pdb
'''
param={
        'zhangshu_base':0.1,
        'jiange_atr':0.2,
        'geshu_ni': 2,
        'zhiying':6,
        'huiche':30,
    }
    
创建网格
    方向 由ma
    张数计算
    间隔计算
    顺势20格 逆势根据参数
开仓交易
    看多时,突破DC20 开始多头网格
    一直顺,顺势开,冻结逆势  盈利=顺势开的
    一直逆,逆势开,冻结顺势,破格止损=逆势开的
    先顺后逆,顺势开,逆势不开,破格止损=顺势开的
    先逆后顺,逆势开,顺势不开,顺势开  盈利=逆势+部分顺势
    
    注意
        开一格后,停止对面一格
        新网格必须破dc20才继续开    
全局交易
    牛市一路涨,开多,止盈或者止损,等继续新高
    牛市一路跌,止损一次后,休眠
    熊市一路跌,开空,止盈或者止损后,等继续新低
    熊市一路涨,止损一次后,休眠
全局概率
    止盈足够大,止损可以大一些.
风险分析
    牛市,破dc20up后,立马跌,
    熊市,破dc20dn后,立马涨,
    拉的过快,开单不及时
    




新增,
超过初始2ATR止损

策略明细:
顺1逆2
顺势开,就停止逆势等张数
逆势开,就停止顺势等张数
追踪止盈
逆势破格止损

优势:
一直顺势,
一直逆势,  破格止损,亏损=逆势开的
先顺后逆,逆势没开,顺势被套,破格止损,亏损=顺势开的
先逆后顺,逆势开的盈利,顺势中断,顺势开仓

先顺后逆后顺,开顺 不开逆  继续开顺=一直顺
线逆后顺后逆,开逆 不开顺,继续开逆=一直逆

止盈止损后要突破极值 继续开

场景:
牛市一直涨,一直顺势
一路开多
牛顶一直跌,逆势止损
一路休息
熊市一直跌,一直顺势
一路开空
熊市一直涨,逆势止损
一路休息
一直涨,打止损后,继续涨

参数要求



'''



def main():
    robot=Kline()
    robot.get_kline_csv(symbol='BTCUSDT', zhouqi='1d')
    robot.get_kline_csv(symbol='ETHUSDT', zhouqi='1d')
    robot.get_kline_csv(symbol='EOSUSDT', zhouqi='1d')
    robot.get_kline_csv(symbol='LTCUSDT', zhouqi='1d')
    robot.get_kline_csv(symbol='ETCUSDT', zhouqi='1d')
    robot.get_kline_csv(symbol='BTCUSDT',zhouqi='1m')
    robot.get_kline_csv(symbol='ETHUSDT',zhouqi='1m')
    robot.get_kline_csv(symbol='EOSUSDT',zhouqi='1m')
    robot.get_kline_csv(symbol='LTCUSDT',zhouqi='1m')
    robot.get_kline_csv(symbol='ETCUSDT',zhouqi='1m')

    # robot=Policyshunshiwg()
    # param={
    #     'zhangshu_base':0.05,
    #     'jiange_atr':0.2,
    #     'zhisun_atr': 2,
    #     'zhiying':9,
    #     'huiche':30,
    # }
    # robot.start('eth',"2018-06-18 23:40","2020-06-18 23:59",param)
if __name__ == '__main__':
    main()
    exit()