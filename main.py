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
def piliang():
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
    # dm.order_piliang(
    #     coinname='eos',
    #     price_start=3.071,
    #     jiange=0.002,
    #     times=132,
    #     volume=1,
    #     direction='sell',
    #     offset='open',
    # )
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
        price_start=10450,
        jiange=10,
        times=30,
        volume=1,
        direction='sell',
        offset='open',
    )
    dm.order_piliang(
        coinname='btc',
        price_start=10750,
        jiange=10,
        times=47,
        volume=1,
        direction='sell',
        offset='close',
    )


def main():
    robot=Policywgma60ma91()
    param={
        'zhangshu':0.03,
        'jiange':0.1,#每格间距多少atr
        'zhiying':8,#止盈比例
        'huiche':20,#回撤比例
        'zhisun':1,#逆势多少atr
        'sleep':1,
    }
    robot.start(
        coinname='eth',
        date_start='2018-09-15 12:00',
        date_end='2019-12-15 12:00',
        param=param
    )


if __name__ == '__main__':
    main()
    # piliang()
