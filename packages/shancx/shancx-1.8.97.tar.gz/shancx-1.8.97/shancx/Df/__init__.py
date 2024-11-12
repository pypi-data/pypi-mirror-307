#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2024/10/17 上午午10:40
# @Author : shancx
# @File : __init__.py
# @email : shanhe12@163.com

import numpy as np
def getmask(df,col = 'PRE1_r'):
    df[col] = df[col].mask(df[col] >= 9999, np.nan)     
    df = df.dropna()
    return df

def Type(df_,col = 'stationID'):
    df_['stationID'] = df_['stationID'].astype("str")
    return df_

