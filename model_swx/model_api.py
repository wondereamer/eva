#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 16:37:28 2019

@author: vasili
"""
import os
import numpy as np
from corr_analysis import correlation_analysis
from extract import extract_economic_news


from keras.models import load_model
root_dir = os.path.abspath(os.path.dirname(__file__))

correlation_analysis = correlation_analysis
extract_economic_news = extract_economic_news

model_path = os.path.join(root_dir,'model','model.h5')
def predict(data):
    """
    预测美元的走势，使用到的数据和特征 9个特征
    '开盘价(元)', '最高价(元)', '最低价(元)', '收盘价(元)' ==>DollarIndex.xlsx
    'Benchmark interest rate','cpi','Retail sales','Non-agricultural employment','gdp' == >基准利率.xls
    
    输入的数据的shape为（5，9），eg：
    [[  85.32,   85.32,   85.32,   85.32,   14.  ,   13.9 ,  252.4 ,   62.  , 1702.3 ],
       [  85.26,   85.26,   85.26,   85.26,   13.89,   13.9 ,  252.4 ,   62.  , 1702.3 ],
       [  85.23,   85.23,   85.23,   85.23,   14.  ,   13.9 ,  252.4 ,   62.  , 1702.3 ],
       [  84.79,   84.79,   84.79,   84.79,   14.  ,   13.9 ,  252.4 ,   62.  , 1702.3 ],
       [  85.07,   85.07,   85.07,   85.07,   13.86,   13.9 ,  252.4 ,   62.  , 1702.3 ]]
    输出下一天的值
    """
    data = np.expand_dims(data, axis=0)
    model = load_model(model_path)
    return model.predict(data)[0][0]