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

def main():
    robot=HuobiDM()
    robot.order_piliang(
        coinname='eos',
        price_start=3.123,
        jiange=0.002,
        times=200,
        volume=1,
        direction='sell',
        offset='open',
        jingdu=3
    )

if __name__ == '__main__':
    main()
    exit()