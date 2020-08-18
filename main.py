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
        'zhangshu':0.1,
        'jiange':0.1,

    }
    robot.start('eth',"2018-06-18 23:40","2019-11-18 23:59",param)

if __name__ == '__main__':
    main()