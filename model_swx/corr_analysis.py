#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 11:15:33 2019

@author: vasili
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
from pandas.tseries.offsets import *
import sys



def corr_value(df,end,lookback=1):
    try:
        strp_end = datetime.datetime.strptime(end, "%Y-%m-%d")
        strp_begin = strp_end - DateOffset(months=lookback)
        strf_begin = datetime.datetime.strftime(strp_begin, "%Y-%m-%d")

    except:
        raise Exception('input format error')
    df = df[(df['date'] > strf_begin) & (df['date'] < end)]
    corr = df[['value1','value2']].corr()['value1']['value2']
    return corr

def show_plot(data):

    fig,ax1 = plt.subplots(1,1)
    ax1.set_ylabel('Correlation Value ',fontsize=12)
    ax1.set_xlabel('Date time ',fontsize=12)
    plt.plot(data['value'])

    
    date_list = data['date'].values
    ax1.set_xticks([x for x in range(len(date_list))])
    for label in ax1.set_xticklabels([date for date in date_list], rotation='vertical'):#[::2]
        label.set_visible(True)
    plt.legend(['Correlation'])
    plt.show()


def valid_date(df,time):
    """如果time时间的数据为空，则回退，直到数据不为空"""
    d = df[df['date'] == time]
    i = 0
    while d.empty:
        t1 = datetime.datetime.strptime(time, "%Y-%m-%d")
        t2 = datetime.datetime.strftime(t1-datetime.timedelta(days=1), "%Y-%m-%d")
        d = df[df['date'] == t2]
        time = t2
        i += 1
        if i >=7:
            print('数据为空')
            print(time)
            break
    return d


def merge_data(data1, data2):

    if isinstance(data1, list) and isinstance(data2, list):
        data1 = pd.DataFrame(data1, columns=['date','value1'])
        data2 = pd.DataFrame(data2, columns=['date','value2'])

    merged_data = pd.merge(data1, data2, on=['date'])

    merged_data.reset_index(inplace=True)
    
    return merged_data

def correlation_analysis(data1, data2, start_dt, end_dt,peroids='M',plot=False):
    '''
    这里的period 为坐标轴上面显示的间隔，即隔多久计算一次相关性，取值范围【M W D 】
    https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#offset-aliases
    return:
        返回一个列表，每个元素为一个四元组（时间，皮尔逊相关系数，data1_value,data2_value）
        
    分析两个时序数据在某个时间段的相关性
    Parameters
    ----------
    data1 : ([datetime], [float])
    数据元组1，包含时间和数值数组。 data2 : ([datetime], [float]) 数据元组2，包含时间和数值数组。
     start_dt : str
    开始时间
    end_dt : str
    介绍时间
    period: str
    ⽐比对单位，取值week, month, quarter, year
     Returns
     -------
     correlation : ([datetime], [float], float)
    不不同时间段的相关性
"""
    '''
    if not end_dt:
        end_dt = datetime.datetime.strftime(datetime.date.today()-datetime.timedelta(days=1), "%Y-%m-%d")
    try:
        datetime.datetime.strptime(start_dt, "%Y-%m-%d")
        datetime.datetime.strptime(end_dt, "%Y-%m-%d")
    except:
         raise Exception(f'input start_dt or end_dt {start_dt} format error,%Y-%m-%d expected')
         
    df = merge_data(data1, data2)
#    df = df[(df['date'] >= start_dt) & (df['date'] <= end_dt)]
    date_list = pd.date_range(start = start_dt,end=end_dt,freq=peroids)

    result = []
    for d in date_list:
        point = datetime.datetime.strftime(d, "%Y-%m-%d")
        value = corr_value(df,point)

        try:
            tmp = valid_date(df, point)
            value1 = tmp['value1'].values[0]
            value2 = tmp['value2'].values[0]
            result.append((point,value,value1,value2))
        except:
            print(f'边界值:{point}')
    if plot:
        result_df = pd.DataFrame(result,columns=['date','value','value1','value2'])
        show_plot(result_df)
    
    return result


if __name__ == "__main__":

    df = pd.read_excel('DollarIndex.xlsx')
    df = df[[ '日期', '开盘价(元)', '最高价(元)', '最低价(元)', '收盘价(元)']]
    df.dropna(inplace=True)
    df.columns = ['date','open','hight','low','close']
    #df.set_index('date',inplace=True)
    #df['date'] = pd.to_datetime(df['date'])
    # 模拟数据
    data1 = df[['date','open']].values.tolist()
    
    
    data2 = df[['date','close']].values.tolist()
    
    correlation_analysis(data1,data2,'1999-12-05','2001-01-01','M',plot=True)

