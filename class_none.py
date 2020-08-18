# @Time : 2020/5/4 3:52 
# @Author : bufeetu
# @File : class_none.py
import time, datetime
import os
import requests
import json
import pymysql
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#注释完毕
class Tool:
    list_jieguo=[]
    def __init__(self):
        self.list_jieguo=[]
    def dict_tiaoshi(self,coinname,yaoqiu_nianhua,yaoqiu_huiche):
        self.list_ok=[]
        rate_nianhuahuichechicang_max=0
        for i in range(len(self.list_jieguo)):
            # print(i)
            # print(self.list_jieguo[i])
            nianhua=float(self.list_jieguo[i]['nianhua'])
            huichemax=float(self.list_jieguo[i]['huichemax'])
            chicang=float(self.list_jieguo[i]['chicang'])
            # if nianhua>yaoqiu_nianhua and huichemax<yaoqiu_huiche:
            #     self.list_ok.append(self.list_jieguo[i])
            rate_nianhuahuichechicang = nianhua/huichemax/chicang
            if self.list_ok==[] or rate_nianhuahuichechicang>rate_nianhuahuichechicang_max:
                self.list_ok.append(self.list_jieguo[i])
                rate_nianhuahuichechicang_max=rate_nianhuahuichechicang
                print(rate_nianhuahuichechicang_max)
        i=0
        nianhua_total=0
        huichemax_total=0
        maup_total=0
        madn_total=0
        jiange_total=0
        zhiying_total=0
        zhisun_total=0
        zhisunatr_total=0
        huiche_total=0
        for i in range(len(self.list_ok)):
            print(i)
            print(self.list_ok[i])
            nianhua_total+=float(self.list_ok[i]['nianhua'])
            huichemax_total+=float(self.list_ok[i]['huichemax'])

            maup_total += float(self.list_ok[i]['maup'])
            madn_total += float(self.list_ok[i]['madn'])
            jiange_total += float(self.list_ok[i]['jiange'])
            zhiying_total += float(self.list_ok[i]['zhiying'])
            zhisun_total += float(self.list_ok[i]['zhisun'])
            zhisunatr_total += float(self.list_ok[i]['zhisunatr'])
            huiche_total += float(self.list_ok[i]['huiche'])
        num=len(self.list_ok)
        nianhua_aver=nianhua_total/num
        huichemax_aver=huichemax_total/num

        maup_aver = maup_total / num
        madn_aver = madn_total / num
        jiange_aver = jiange_total / num
        zhiying_aver = zhiying_total / num
        zhisun_aver = zhisun_total / num
        zhisunatr_aver = zhisunatr_total / num
        huiche_aver = huiche_total / num

        print(coinname+'个数'+str(num))
        print('平均年化'+str(nianhua_aver))
        print('平均最大回撤'+str(huichemax_aver))
        print('maup'+str(maup_aver))
        print('madn'+str(madn_aver))
        print('jiange'+str(jiange_aver))
        print('zhiying'+str(zhiying_aver))
        print('zhisun'+str(zhisun_aver))
        print('zhisunatr'+str(zhisunatr_aver))
        print('huiche'+str(huiche_aver))

    def jiexi_dict(self,line):
        line = str(line).replace("nh", "&")
        line = str(line).replace("hc", "&")
        line = str(line).replace("cc", "&")
        line = str(line).replace("sl", "&")
        line = str(line).replace("yk", "&")
        line = str(line).replace("$", "&")
        lista=str(line).split('&')
        dicta={
            'coinname':lista[0],
            'nianhua':lista[1],
            'huichemax':lista[2],
            'chicang':lista[3],
            'shenglv':lista[4],
            'yingkui':lista[5],
            'maup':lista[6],
            'madn':lista[7],
            'jiange':lista[8],
            'zhiying':lista[9],
            'zhisun':lista[10],
            'zhisunatr':lista[11],
            'huiche':lista[12],
        }
        self.list_jieguo.append(dicta)
    def fenxi_png(self):
        coinname='etc'
        yaoqiu_nianhua=130
        yaoqiu_huiche=25
        print('start')
        f = open("zongjie"+coinname+".txt", "r")  # 设置文件对象
        line = f.readline()
        line = line[:-1]
        while line:  # 直到读取完文件
            print(line)
            self.jiexi_dict(line)
            line = f.readline()  # 读取一行文件，包括换行符
            line=str(line).replace("\n", "")
        f.close()  # 关闭文件
        self.dict_tiaoshi(coinname,yaoqiu_nianhua,yaoqiu_huiche)
