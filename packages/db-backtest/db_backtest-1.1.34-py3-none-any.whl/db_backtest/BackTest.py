# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time as Time
import os
import matplotlib.pyplot as plt
import dbfactor_analyzer as db
from chinese_calendar import is_holiday
from datetime import datetime,timedelta
from functools import cached_property
from .plot_utils import print_table
import warnings
from tqdm import tqdm
from .prepare import max_drawdown, annualized_return, annualized_volatility, sharpe_ratio
warnings.filterwarnings('ignore')


import seaborn as sns
sns.set_style('darkgrid')

class BackTest_DF(object):

    def __init__(self, signal,close_hfq,initial_money,coupon_interest_rate,turnover_rate,stamp_rate,other_close=pd.DataFrame([]),chengfen_filepath=None):

        '''
        signal: 交易信号,可以是list或者dataframe
                包括日期、交易方向、股票代码、数量、价格、配对交易序号
                交易方向：
                1: 买入
                2: 卖出
                3: 融资买入
                4: 融券卖出
                5: 买券还
        close_hfq: 收盘价,为dataframe,index为日期,columns为股票代码
        initial_money: 回测起始资金
        coupon_interest_rate: 券息率,可以是一个数,一个字典,一个dataframe,一个series
        turnover_rate: 换手费率,可以是一个数,一个字典,一个dataframe,一个series
        stamp_rate: 印花税率,可以是一个数,一个字典,一个dataframe,一个series
        other_close: 其他收盘价,为dataframe,index为日期,columns为代码(比如期货、指数、ETF等的收盘价)
        chengfen_filepath:成分股文件所在地址，没有就不画图
        '''
        #如果signal的类型是list
        signal_copy=signal.copy()
        if isinstance(signal, list):
            #将signal转换成dataframe，列名为日期，交易方向，股票代码，数量, 价格
            self.signal = pd.DataFrame(signal_copy,columns=['date','direction','code','amount','price','pairs'])
            #将日期转换成datetime格式
            self.signal['date'] = pd.to_datetime(self.signal['date'])
            self.signal['direction']=self.signal['direction'].astype(int) 
            self.signal['amount']=self.signal['amount'].astype(np.float64)
            self.signal['price']=self.signal['price'].astype(np.float64)
            self.signal['pairs']=self.signal['pairs'].astype(int) 
        #如果signal的类型是dataframe
        elif isinstance(signal, pd.DataFrame):
            self.signal = signal_copy
            #列名改为日期，交易方向，股票代码，数量，价格
            self.signal.columns = ['date','direction','code','amount','price','pairs']
            #将日期转换成datetime格式
            self.signal['date'] = pd.to_datetime(self.signal['date'])
            self.signal['direction']=self.signal['direction'].astype(int) 
            self.signal['amount']=self.signal['amount'].astype(np.float64)
            self.signal['price']=self.signal['price'].astype(np.float64)
            self.signal['pairs']=self.signal['pairs'].astype(int) 

        self.signal.replace([np.inf,-np.inf],np.nan,inplace=True)
        self.signal.dropna(inplace=True)
        self.signal.reset_index(drop=True,inplace=True)

        #获取self.signal中date最小和最大的日期
        self.start_date=self.signal['date'].min()
        self.end_date=self.signal['date'].max() 
        self.close_hfq = close_hfq
        self.close_hfq.index = pd.to_datetime(self.close_hfq.index)
        if len(other_close):
            self.ZS_close = other_close.copy()
            self.ZS_close.index = pd.to_datetime(self.ZS_close.index)
            self.ZS_close.index=self.close_hfq.index
            self.close_new=pd.concat([self.close_hfq,self.ZS_close],axis=1)
        else:
            self.close_new=self.close_hfq.copy()
        self.initial_money = initial_money
        self.coupon_interest_rate = coupon_interest_rate
        self.turnover_rate = turnover_rate
        self.stamp_rate = stamp_rate
        self.chengfen_filepath=chengfen_filepath

    @cached_property
    def tradedays_list(self):
        '''
        计算两个日期间的工作日（交易日）
        '''
        startdate=self.start_date
        enddate=self.end_date
        if type(startdate)==str:
            startdate = pd.to_datetime(startdate)
        if type(enddate)==str:
            enddate = pd.to_datetime(enddate)
        
        tradedayslist=[]
        while True:
            if startdate > enddate:
                break
            if is_holiday(startdate) or startdate.weekday()>=5 or startdate==pd.to_datetime('2024/02/09'):
                startdate += timedelta(days=1)
                continue
            tradedayslist.append(startdate)
            startdate += timedelta(days=1)

        return tradedayslist
    

    def signal_process(self,signal_by_pairs):
        signal_by_pairs_copy=signal_by_pairs.copy()
        signal_by_pairs_copy['code_date']=signal_by_pairs_copy['code'].astype(str)+signal_by_pairs_copy['date'].astype(str)
        signal_repeat=signal_by_pairs_copy[signal_by_pairs_copy['code_date'].isin(signal_by_pairs_copy['code_date'].value_counts()[signal_by_pairs_copy['code_date'].value_counts()>1].index)]
        signal_by_pairs_copy=signal_by_pairs_copy[~signal_by_pairs_copy['code_date'].isin(signal_repeat['code_date'])]

        return signal_by_pairs_copy,signal_repeat

    def backtestdf_pairs(self,signal_by_pairs):
        '''
        得到现金资产负债表
        形式：
        index: 双索引,level0为股票代码, level1为全部交易日期
        columns: 交易方向、数量、交易价格、收盘价、券息率、换手费率、印花税率、现金、资产、负债、券息、换手费、印花税、净值
        '''
        #获取交易日列表
        tradedayslist =self.tradedays_list
        signal_by_pairs.reset_index(drop=True,inplace=True)
        #重置signal_by_pairs的索引
        #获取股票代码列表
        code_list = signal_by_pairs['code'].unique()
        #构建双索引
        index = pd.MultiIndex.from_product([code_list,tradedayslist],names=['code','date'])
        #构建空的dataframe
        backtest_df = pd.DataFrame(index=index,columns=['交易方向','数量','交易价格','券息率','换手费率','印花税率','当日现金流','当日资产(股数)',
        '当日负债(股数)','换手费','印花税'])     
        
        for i in range(len(signal_by_pairs)): #使用到了索引
            backtest_df.loc[(signal_by_pairs['code'][i],signal_by_pairs['date'][i]),'交易方向'] = signal_by_pairs['direction'][i]
            backtest_df.loc[(signal_by_pairs['code'][i],signal_by_pairs['date'][i]),'数量'] = signal_by_pairs['amount'][i]
            backtest_df.loc[(signal_by_pairs['code'][i],signal_by_pairs['date'][i]),'交易价格'] = signal_by_pairs['price'][i]

        #如果换手费率是一个数
        if isinstance(self.turnover_rate, (int,float)):
            backtest_df['换手费率'] = self.turnover_rate
            #如果换手费率是一个字典，key为股票代码，value为换手费率
        elif isinstance(self.turnover_rate, dict):   
            ss=pd.Series(self.turnover_rate)
            backtest_df['换手费率'] = backtest_df.index.get_level_values(0).map(ss) 
        #如果换手费率是一个dataframe，index为股票代码，columns为交易日期
        elif isinstance(self.turnover_rate, pd.DataFrame):
            backtest_df['换手费率'] = self.turnover_rate.stack()
            #如果换手费率是一个series，index为股票代码，value为换手费率
        elif isinstance(self.turnover_rate, pd.Series):
            backtest_df['换手费率'] = backtest_df.index.get_level_values(0).map(self.turnover_rate)
        
        #如果印花税率是一个数
        if isinstance(self.stamp_rate, (int,float)):
            backtest_df['印花税率'] = self.stamp_rate
            #如果印花税率是一个字典，key为股票代码，value为印花税率
        elif isinstance(self.stamp_rate, dict):
            ss=pd.Series(self.stamp_rate)
            backtest_df['印花税率'] = backtest_df.index.get_level_values(0).map(ss)
        #如果印花税率是一个dataframe，index为股票代码，columns为交易日期
        elif isinstance(self.stamp_rate, pd.DataFrame):
            backtest_df['印花税率'] = self.stamp_rate.stack()
        #如果印花税率是一个series，index为股票代码，value为印花税率
        elif isinstance(self.stamp_rate, pd.Series):
            backtest_df['印花税率'] = backtest_df.index.get_level_values(0).map(self.stamp_rate)

        backtest_df.loc[backtest_df['交易方向']==1,'当日现金流'] = -backtest_df['数量']*backtest_df['交易价格']
        backtest_df.loc[backtest_df['交易方向']==1,'当日资产(股数)'] = backtest_df['数量']
        #如果交易方向为2(卖出)，现金为数量*股价，资产为负数量
        backtest_df.loc[backtest_df['交易方向']==2,'当日现金流'] = backtest_df['数量']*backtest_df['交易价格']
        backtest_df.loc[backtest_df['交易方向']==2,'当日资产(股数)'] = -backtest_df['数量']
        #如果交易方向为3(融资买入),暂不做处理
        #如果交易方向为4(融券卖出),现金为数量*股价，负债为数量
        backtest_df.loc[backtest_df['交易方向']==4,'当日现金流'] = backtest_df['数量']*backtest_df['交易价格']
        backtest_df.loc[backtest_df['交易方向']==4,'当日负债(股数)'] = backtest_df['数量']
        #如果交易方向为5(买还),现金为负数量*股价，负债为负数量
        backtest_df.loc[backtest_df['交易方向']==5,'当日现金流'] = -backtest_df['数量']*backtest_df['交易价格']
        backtest_df.loc[backtest_df['交易方向']==5,'当日负债(股数)'] = -backtest_df['数量']

        #backtest_df中所有的空值填为0
        backtest_df.fillna(0,inplace=True)
        #换手费等于换手费率*现金流的绝对值
        backtest_df['换手费'] = backtest_df['换手费率']*backtest_df['当日现金流'].abs()
        #当交易方向为偶数时，印花税等于印花税率*现金流的绝对值，当交易方向为奇数时，印花税为0
        backtest_df['印花税'] = backtest_df['印花税率']*backtest_df['当日现金流'].abs()*(backtest_df['交易方向']%2==0)

        return backtest_df
    
    def backtestdf(self,signal_by_pairs,close_hfq):
        signal_pairs=self.signal_process(signal_by_pairs)[0]
        result1=self.backtestdf_pairs(signal_pairs)
        #得到result1中交易方向为1和2的股票代码
        signal_repeat=self.signal_process(signal_by_pairs)[1]
        if signal_repeat.shape[0]!=0:
            signal_repeat['序列']=np.arange(1,len(signal_repeat)+1)
            result2=signal_repeat.groupby(['序列']).apply(lambda x:self.backtestdf_pairs(x))
            result2.index=result2.index.droplevel(0)
            result3=pd.concat([result1,result2],axis=0)
            #long_stock=list(result3[result3['交易方向'].isin([1,2])].index.get_level_values(0).unique())
            result4=result3[['当日现金流','当日资产(股数)','当日负债(股数)','换手费','印花税']]
            def sum_byday(group):
                return group.groupby(['date']).sum()
            result5=result4.groupby(level=0).apply(lambda x: sum_byday(x))
        else:
            #long_stock=list(result1[result1['交易方向'].isin([1,2])].index.get_level_values(0).unique())
            result5=result1[['当日现金流','当日资产(股数)','当日负债(股数)','换手费','印花税']]

        #signal中的股票代码必须在close中
        if not signal_by_pairs['code'].isin(self.close_new.columns).all():
            string=set(signal_by_pairs['code'])-set(self.close_new.columns)                                
            raise ValueError(f'{string}股票代码不在close中')
        #signal中的日期必须在close中
        if not signal_by_pairs['date'].isin(self.close_hfq.index).all():
            string=set(signal_by_pairs['date'])-set(self.close_hfq.index)
            raise ValueError(f'{string}日期不在close中')   
        result5['收盘价'] = close_hfq     
  
        #对于result5中level0为long_stock的股票，收盘价用close_hfq_copy中对应的值代替
        #result5.loc[result5.index.get_level_values(0).isin(long_stock),'收盘价'] = close_bfq.loc[close_bfq.index.get_level_values(0).isin(long_stock)]

        #如果券息率是一个数
        if isinstance(self.coupon_interest_rate, (int,float)):
            result5['券息率'] = self.coupon_interest_rate
        #如果券息率是一个字典，key为股票代码，value为券息率
        elif isinstance(self.coupon_interest_rate, dict):
            ss=pd.Series(self.coupon_interest_rate)
            result5['券息率'] = result5.index.get_level_values(0).map(ss)
        #如果券息率是一个dataframe，index为股票代码，columns为交易日期
        elif isinstance(self.coupon_interest_rate, pd.DataFrame):
            result5['券息率'] = self.coupon_interest_rate.stack()
        #如果券息率是一个series，index为股票代码，value为券息率
        elif isinstance(self.coupon_interest_rate, pd.Series):
            result5['券息率'] = result5.index.get_level_values(0).map(self.coupon_interest_rate)
        
        #新增当日资产(价格)列，对每个股票求出按日累加的当日资产(股数)然后乘以收盘价(不复权)
        result5['所持资产(价格)'] = result5.groupby(level=0)['当日资产(股数)'].cumsum()*result5['收盘价']
        #新增所持负债(价格)列，对每个股票求出按日累加的当日负债(股数)然后乘以收盘价(不复权)
        result5['所持负债(价格)'] = result5.groupby(level=0)['当日负债(股数)'].cumsum()*result5['收盘价']
        #新增当日所持负债券息，用所持负债(价格)*券息率得到每日券息
        result5['当日所持负债券息'] = result5['所持负债(价格)']*result5['券息率']/360
        #当日所持负债券息中小于0的部分用0代替
        result5.loc[result5['当日所持负债券息']<0,'当日所持负债券息'] = 0
        #新增个股当日现金流净值列，计算现金流-换手费-印花税费-当日负债券息
        result5['个股当日现金流净值'] = result5['当日现金流']-result5['换手费']-result5['印花税']-result5['当日所持负债券息']
        #按照日期分组，统计每日所有股票现金流净值、当日资产(价格)、当日负债(价格)的和，输出为一张新的df
        result_df = result5.groupby(level=1).agg({'个股当日现金流净值':'sum','所持资产(价格)':'sum','所持负债(价格)':'sum'})
        #result_df中新增所持现金流列，为个股当日现金流净值的累计值
        result_df['所持现金流'] = result_df['个股当日现金流净值'].cumsum()
        #result_df中新增净值列，为所持资产(价格)减去所持负债(价格)再加上所持现金流
        result_df['净值'] = result_df['所持资产(价格)']-result_df['所持负债(价格)']+result_df['所持现金流']

        return result_df
    
    def middletable(self,signal_by_pairs,close_hfq):
        signal_pairs=self.signal_process(signal_by_pairs)[0]
        result1=self.backtestdf_pairs(signal_pairs)
        #得到result1中交易方向为1和2的股票代码
        signal_repeat=self.signal_process(signal_by_pairs)[1]
        if signal_repeat.shape[0]!=0:
            signal_repeat['序列']=np.arange(1,len(signal_repeat)+1)
            result2=signal_repeat.groupby(['序列']).apply(lambda x:self.backtestdf_pairs(x))
            result2.index=result2.index.droplevel(0)
            result3=pd.concat([result1,result2],axis=0)
            #long_stock=list(result3[result3['交易方向'].isin([1,2])].index.get_level_values(0).unique())
            result4=result3[['当日现金流','当日资产(股数)','当日负债(股数)','换手费','印花税']]
            def sum_byday(group):
                return group.groupby(['date']).sum()
            result5=result4.groupby(level=0).apply(lambda x: sum_byday(x))
        else:
            #long_stock=list(result1[result1['交易方向'].isin([1,2])].index.get_level_values(0).unique())
            result5=result1[['当日现金流','当日资产(股数)','当日负债(股数)','换手费','印花税']]

        #signal中的股票代码必须在close中
        if not signal_by_pairs['code'].isin(self.close_new.columns).all():
            raise ValueError('股票代码不在close中')
        #signal中的日期必须在close中
        if not signal_by_pairs['date'].isin(self.close_new.index).all():
            raise ValueError('日期不在close中')   
        result5['收盘价'] = close_hfq     
        #对于result5中level0为long_stock的股票，收盘价用close_hfq_copy中对应的值代替
        #result5.loc[result5.index.get_level_values(0).isin(long_stock),'收盘价'] = close_bfq.loc[close_bfq.index.get_level_values(0).isin(long_stock)]

        #如果券息率是一个数
        if isinstance(self.coupon_interest_rate, (int,float)):
            result5['券息率'] = self.coupon_interest_rate
        #如果券息率是一个字典，key为股票代码，value为券息率
        elif isinstance(self.coupon_interest_rate, dict):
            ss=pd.Series(self.coupon_interest_rate)
            result5['券息率'] = result5.index.get_level_values(0).map(ss)
        #如果券息率是一个dataframe，index为股票代码，columns为交易日期
        elif isinstance(self.coupon_interest_rate, pd.DataFrame):
            result5['券息率'] = self.coupon_interest_rate.stack()
        #如果券息率是一个series，index为股票代码，value为券息率
        elif isinstance(self.coupon_interest_rate, pd.Series):
            result5['券息率'] = result5.index.get_level_values(0).map(self.coupon_interest_rate)
        
        #新增当日资产(价格)列，对每个股票求出按日累加的当日资产(股数)然后乘以收盘价(不复权)
        result5['所持资产(价格)'] = result5.groupby(level=0)['当日资产(股数)'].cumsum()*result5['收盘价']
        #新增所持负债(价格)列，对每个股票求出按日累加的当日负债(股数)然后乘以收盘价(不复权)
        result5['所持负债(价格)'] = result5.groupby(level=0)['当日负债(股数)'].cumsum()*result5['收盘价']
        #新增当日所持负债券息，用所持负债(价格)*券息率得到每日券息
        result5['当日所持负债券息'] = result5['所持负债(价格)']*result5['券息率']/360
        #当日所持负债券息中小于0的部分用0代替
        result5.loc[result5['当日所持负债券息']<0,'当日所持负债券息'] = 0
        #新增个股当日现金流净值列，计算现金流-换手费-印花税费-当日负债券息
        result5['个股当日现金流净值'] = result5['当日现金流']-result5['换手费']-result5['印花税']-result5['当日所持负债券息']

        return result5

    def Net_sheet(self):
        '''
        得到每日净值表
        '''
 
        close_hfq_copy=self.close_new.stack(dropna=False)
        close_hfq_copy.index = close_hfq_copy.index.swaplevel(0,1)
        tqdm.pandas(desc='begin calc net')
        Net_table=self.signal.groupby('pairs').progress_apply(lambda x:self.backtestdf(signal_by_pairs=x,close_hfq=close_hfq_copy))
        #将net_sheet按照date分组，对每组求和
        Net_table=Net_table.groupby(level=1).sum()
        #对net_table净值列的第一个值加上self.initial_money
        Net_table['净值'] += float(self.initial_money)

        return Net_table
    

    def stack_line_plot(self,save_path=None):

        close_hfq_copy=self.close_new.stack(dropna=False)
        close_hfq_copy.index = close_hfq_copy.index.swaplevel(0,1)
        tqdm.pandas(desc='begin calc middle_table')
        middle_table=self.signal.groupby('pairs').progress_apply(lambda x:self.middletable(signal_by_pairs=x,close_hfq=close_hfq_copy))
        middle_table.reset_index(inplace=True)
        #将date列设为索引
        middle_table.set_index('date',inplace=True)

        chengfen_filepath =self.chengfen_filepath
        #中间表存放路径
        zhongjianbiao = middle_table.copy()
     
        zhongjianbiao=zhongjianbiao[['code','所持资产(价格)','所持负债(价格)']]
        #去掉空值
        zhongjianbiao.dropna(inplace=True)

        '''
        导入所有成分股列表和权重
        '''
        chengfen_file_list = os.listdir(chengfen_filepath)
        chengfen_file_list = [file for file in chengfen_file_list if not file.startswith('~')]
        chengfen_list = list(map(lambda x:x.replace('.xlsx',''),chengfen_file_list))
        #print(chengfen_list)
        
        # 导入所有因子文件，文件名作为变量名
        for filename in chengfen_file_list:
            path = os.path.join(chengfen_filepath, filename)
            chengfen_name = filename.replace('.xlsx','')
            #print(chengfen_name)
            globals()[chengfen_name] = pd.DataFrame(pd.read_excel(path,index_col='date',engine='openpyxl'))
            index_time_list=[]
            for index_time in globals()[chengfen_name].index.tolist():
                index_time_list.append(Time.strftime("%Y/%m/%d",Time.strptime(index_time,"%Y-%m-%d"))) #实现日期的格式化
            globals()[chengfen_name].index=index_time_list
            globals()[chengfen_name] = globals()[chengfen_name].sort_index()


        #统计多头空头数据
        zhongjianbiao_all_day_buy=pd.DataFrame()
        zhongjianbiao_all_day_sell=pd.DataFrame()

        #统计不属于成分股的多头空头数据
        zhongjianbiao_all_day_buy_not_chengfen=[]
        zhongjianbiao_all_day_sell_not_chengfen=[]

        for date in zhongjianbiao.index.unique():
            zhongjianbiao_simple_day=zhongjianbiao.loc[date]
            zhongjianbiao_simple_day.set_index('code',inplace=True)

            simple_day_index_buy=pd.DataFrame(index=[date])
            simple_day_index_sell=pd.DataFrame(index=[date])

            for chengfen_name in chengfen_list:
                if chengfen_name == '932000.CSI':
                    #print('932000.CSI')
                    chengfen_data = globals()[chengfen_name].loc['2023/08/31']
                    zhongjianbiao_simple_day['市值权重']=chengfen_data.set_index('股票代码')['权重']
                    simple_day_index_buy[chengfen_name] = zhongjianbiao_simple_day.dropna()['所持资产(价格)'].sum()
                    simple_day_index_sell[chengfen_name] = -zhongjianbiao_simple_day.dropna()['所持负债(价格)'].sum()
                else:
                    #print(chengfen_name)
                    #找出离time最近的指数成分权重
                    #找出最近时间
                    df=globals()[chengfen_name]
                    df.index = pd.to_datetime(df.index)
                    nearest_time = df[df.index<pd.to_datetime(date)].index[-1]
                    chengfen_data = globals()[chengfen_name].loc[nearest_time]
                    zhongjianbiao_simple_day['市值权重']=chengfen_data.set_index('股票代码')['权重']
                    simple_day_index_buy[chengfen_name] = zhongjianbiao_simple_day.dropna()['所持资产(价格)'].sum()
                    simple_day_index_sell[chengfen_name] = -zhongjianbiao_simple_day.dropna()['所持负债(价格)'].sum()


            #非成分股数据
            simple_day_index_buy_not_chengfen=zhongjianbiao_simple_day[zhongjianbiao_simple_day['市值权重'].isnull()]['所持资产(价格)'].sum()
            simple_day_index_sell_not_chengfen=-zhongjianbiao_simple_day[zhongjianbiao_simple_day['市值权重'].isnull()]['所持负债(价格)'].sum()

            zhongjianbiao_all_day_buy=pd.concat([zhongjianbiao_all_day_buy,simple_day_index_buy],axis=0)
            zhongjianbiao_all_day_sell=pd.concat([zhongjianbiao_all_day_sell,simple_day_index_sell],axis=0)
            zhongjianbiao_all_day_buy_not_chengfen.append(simple_day_index_buy_not_chengfen)
            zhongjianbiao_all_day_sell_not_chengfen.append(simple_day_index_sell_not_chengfen)
            

        #绘制多头堆积折线图数据
        #绘制多头堆积折线图数据
        x=np.unique(zhongjianbiao.index).tolist()
        y1=np.array(zhongjianbiao_all_day_buy['000016.SH'])
        y2=np.array(zhongjianbiao_all_day_buy['000300.SH'])
        y3=np.array(zhongjianbiao_all_day_buy['000905.SH'])
        y4=np.array(zhongjianbiao_all_day_buy['000852.SH'])
        y5=np.array(zhongjianbiao_all_day_buy_not_chengfen)
        y6=np.array(zhongjianbiao_all_day_buy['932000.CSI'])

        #绘制空头堆积折线图数据
        #绘制空头堆积折线图数据
        x=np.unique(zhongjianbiao.index).tolist()
        z1=np.array(zhongjianbiao_all_day_sell['000016.SH'])
        z2=np.array(zhongjianbiao_all_day_sell['000300.SH'])
        z3=np.array(zhongjianbiao_all_day_sell['000905.SH'])
        z4=np.array(zhongjianbiao_all_day_sell['000852.SH'])
        z5=np.array(zhongjianbiao_all_day_sell_not_chengfen)
        z6=np.array(zhongjianbiao_all_day_sell['932000.CSI'])

        labels=['sz50','hs300','zz500','zz1000','others','zz2000']
        # 绘制堆积面积图，并从上而下设置颜色
        plt.stackplot(x, y1, y2, y3,y4,y5,y6,labels=labels,colors=['blue', 'orange', 'yellow', 'red','green','purple'])  #用colors参数添加，单color只能添加一种颜色
        plt.legend(loc="upper right",fontsize='7')
        plt.stackplot(x, z1, z2, z3,z4,z5,z6, labels=labels,colors=['blue', 'orange', 'yellow', 'red','green','purple'])  #用colors参数添加，单color只能添加一种颜色

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

       #plt.show()

  
class BackTest_PLOT(object):
    '''
    绘制净值曲线图
    '''
    def __init__(self,result_dict,initial_money,baseline=None,rf=0.03):
        ''''
        result_dict: result_dict为字典, key为策略名, value为净值表
        baseline: 基准收益净值表,index为时间,至少需要有一列净值列
        initial_money: 初始资金
        rf: 无风险利率
        '''
        self.result_dict = result_dict
        self.baseline = baseline
        self.initial_money = initial_money
        self.rf = rf

    def backtest_plot(self):
        '''
        绘制净值曲线图
        '''
        plt.figure(figsize=(20,6))
        #如果不包含多条净值曲线

        #创建一个空的dataframe
        net_df = pd.DataFrame()
        #遍历result_dict中的每个策略
        for key in self.result_dict.keys():
            #计算每个策略的最大回撤、年化收益率、波动率、夏普比率
            Max_drawdown=max_drawdown(net_table=self.result_dict[key])*100
            Annualized_return=annualized_return(net_table=self.result_dict[key],Imoney=self.initial_money)*100
            Annualized_volatility=annualized_volatility(net_table=self.result_dict[key])*100
            Sharpe_ratio=sharpe_ratio(net_table=self.result_dict[key],Imoney=self.initial_money,Rf=self.rf)
            #将每个策略的最大回撤、年化收益率、波动率、夏普比率存入一个字典
            net_analyze_table = {'max_drawdown(%)':Max_drawdown,'annualized_return(%)':Annualized_return,
                'annualized_volatility(%)':Annualized_volatility,'sharpe_ratio':Sharpe_ratio}
            #将字典转换成dataframe
            net_analyze_table = pd.DataFrame(net_analyze_table,index=[key])
            #将每个策略的净值表和最大回撤、年化收益率、波动率、夏普比率的dataframe合并
            net_df = pd.concat([net_df,net_analyze_table],axis=0)
        print("各策略净值分析")
        print_table(net_df.apply(lambda x: x.round(3)))
            
        for key in self.result_dict.keys():
            result = self.result_dict[key]
            result.index =  pd.to_datetime(result.index)
            plt.plot(result.index.to_numpy(),result['净值'].to_numpy(),linewidth=1.8,label=key)
        if self.baseline is not None:
            self.baseline.index = pd.to_datetime(self.baseline.index)
            plt.plot(self.baseline.index.to_numpy(),self.baseline['净值'].to_numpy(),linewidth=1.8,color='red',label='baseline')    
        #设置图例位置，右上角
        plt.legend(loc='upper right')
        #plt.xticks(self.baseline.index)
        #yticks_values = [-1.5e8, -1.0e8, -0.5e8, 0.0, 0.5e8, 1.0e8, 1.5e8]
        #plt.yticks(yticks_values)
        plt.xlabel('date',fontsize=15,fontweight='bold')
        plt.ylabel('net_value',fontsize=15,fontweight='bold')
        plt.tick_params(colors='black')
        plt.title('Equity Backtesting Curve',fontsize=25,fontweight='bold')
        plt.show()
