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
import pdb



def main():
    # s = '0'
    # n = int(s)
    # pdb.set_trace() #运行到这里会自动暂停
    # print(10/n)


    turtle=Turtle()
    turtle.start('eth',"2018-06-18 23:40","2019-11-18 23:59")
if __name__ == '__main__':
    main()