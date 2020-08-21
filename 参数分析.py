


def log(content):
    print(content)
def trade(price_start,rate_a,rate_b,zhangshu_ni,wg_jiange):
    #获取开单张数  均价  计算收益币数 收益资金 收益率
    if rate_a>0:
        #顺势
        geshu=price_start*rate_a*0.01/wg_jiange
        zhangshu_trade=zhangshu_ni*2*geshu
        price_aver=price_start*rate_a*0.01*0.5+price_start
        print('顺势开仓,张数'+str(zhangshu_trade)+'均价'+str(price_aver))
        
        pass
    pass
def get_zhangshu_ni(fund,mianzhi,param_zhangshu_ni):
    zhangshu_chong=fund/mianzhi
    zhangshu_ni=zhangshu_chong*param_zhangshu_ni
    return int(zhangshu_ni)    
def run(rate_a,rate_b,param={}):
    #定义常量
    fund_start=10000
    price_start=240
    atr=8.7
    mianzhi=10
    #初步计算
    zhangshu_ni=get_zhangshu_ni(fund_start,mianzhi,param['zhangshu_ni'])
    wg_jiange=atr*param['jiange']
    log('逆势张数'+str(zhangshu_ni))
    log('网格间隔'+str(wg_jiange))
    trade(price_start,rate_a,rate_b,zhangshu_ni,wg_jiange)


    

    pass

def main():
    #定义参数
    param={
        'jiange':0.1,
        'zhangshu_ni':0.05,
        'zhiying':5,
        'huiche':0.3,
        'zhisun':-5,
        'zhisun_atr':2,
    }
    rate_a=10
    rate_b=10
    run(rate_a,rate_b,param)

if __name__ == '__main__':
    main()