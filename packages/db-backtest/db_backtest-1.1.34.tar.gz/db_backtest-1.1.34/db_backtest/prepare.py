# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from .plot_utils import print_table


def max_drawdown(net_table):
    '''
    计算最大回撤率
    '''
   
    max_net_value = net_table['净值'].cummax()
    drawdown = -1*(net_table['净值']-max_net_value)/max_net_value
    max_drawdown = drawdown.max()

    return max_drawdown

    
def annualized_return(net_table,Imoney):
    '''
    计算年化对数收益率
    '''

    annualized_return = (net_table['净值'][-1]/Imoney)**(252/len(net_table))-1
    return annualized_return
    
    
def annualized_volatility(net_table):
    '''
    计算对数收益率的年化波动率
    '''

    annualized_volatility = net_table['净值'].pct_change().std()*np.sqrt(252)
    return annualized_volatility

def sharpe_ratio(net_table,Imoney,Rf):
    '''
    计算夏普比率
    '''
    sharpe_ratio = (annualized_return(net_table,Imoney)-Rf)/annualized_volatility(net_table)
    return sharpe_ratio

def plot_net_analyze_table(net_table,Imoney,Rf):
    net_analyze_table = pd.DataFrame()
    net_analyze_table["最大回撤(%)"] = max_drawdown(net_table)*100
    net_analyze_table["年化对数收益率(%)"] =annualized_return(net_table,Imoney)*100
    net_analyze_table["对数收益率年化波动率(%)"] = annualized_volatility(net_table)*100
    net_analyze_table["夏普比率"] = sharpe_ratio(net_table,Rf)
    print("净值分析")
    print_table(net_analyze_table.apply(lambda x: x.round(3)).T)