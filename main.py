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
from HuobiDMService import HuobiDM
from class_policywgma60ma91 import Policywgma60ma91

def main():
    robot=Policywgma60ma91()
    param={
        'zhangshu':0.02,
        'jiange':0.2,
        'zhisun':5,
        'sleep':5,
    }
    robot.start(
        coinname='eth',
        date_start='2018-09-15 12:00',
        date_end='2018-12-15 12:00',
        param=param
    )
    # ACCESS_KEY = 'bb744223-32147a86-56597f7f-ez2xc4vb6n'
    # SECRET_KEY = '8bc9bf60-64d68dfc-2cc3f4f7-b08de'
    # dm = HuobiDM(ACCESS_KEY, SECRET_KEY)
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
    #     price_start=2.7,
    #     jiange=0.002,
    #     times=200,
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
    # dm.order_piliang(
    #     coinname='btc',
    #     price_start=10450,
    #     jiange=10,
    #     times=50,
    #     volume=1,
    #     direction='sell',
    #     offset='open',
    # )

if __name__ == '__main__':
    main()
    exit()