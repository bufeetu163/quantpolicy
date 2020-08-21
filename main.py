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
import pdb



def main():
    robot=Policyshunshiwg()
    param={
        'zhangshu_ni':0.05,
        'jiange':0.2,
        'zhiying':9,
        'huiche':30,
        'zhisun':-5,
        'zhisun_atr':2,

    }
    robot.start('eth',"2018-06-18 23:40","2019-11-18 23:59",param)

if __name__ == '__main__':
    main()