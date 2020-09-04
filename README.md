# quantpolicy

## 策略描述

### 均线策略

- 选择方向

- ```
    price>ma60>ma91  正在上涨
    ma60>price>ma91  上涨中的回调
    ma60>ma91>price   急速下跌,不一定涨
    ma91>ma60>price  正在下跌
    ma91>price>ma60  下跌中的反弹
    price>ma91>ma60  急速拉高,必跌
    ```

    

- 创建网格

- ```
    格数=41
    间隔=jiange*atr
    张数=zhangshu*zhangshu_chong
    方向=如上
    
    
    ```

    

- 交易网格

- 止盈止损

- ```
    被套多少格
    ```

- 休眠

- ```
    平仓后,休息7天或上下波动 sleep*atr
    ```

- 参数

- ```
    jiange
    zhangshu
    zhisun
    sleep
    共四个参数
    目标:方向准确   顺势一直拿  逆势就跑
    方向  解决胜率
    jiange*atr 分散份数,在合理范围内抄底和追涨
    zhangshu  不影响
    zhisun个数 解决盈亏比,控制亏损程度和盈利程度 同时担任了,一直拿和立即跑
    sleep     解决了胜率,控制开仓时         是新的一轮开始需要,等行情出现,避免原地继续亏.
    ```

### 开发进度

- [x] 遍历数据

- [ ] 创建网格

- [ ] ing wait

- [ ] ok

- [ ] close

- [ ] 记录

- [ ] 总结并绘图

- [ ] 参数调优

    

### 

