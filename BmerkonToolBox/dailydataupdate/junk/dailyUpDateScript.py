# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 16:04:47 2017

@author: Administrator
"""

import pandas as pd 
import numpy as np
import pickle
import sys
sys.path.append('D:/pythonwork/MyToolBox/DataImport/')
sys.path.append('D:/pythonwork/MyToolBox/bt_algos/')
from JuyuanQuery import JuYuanDB

import pyodbc as db_odbc
import psycopg2 as db_pgs

import time
import datetime
from pathlib import Path
#%% 更新分钟级数据库

#%% 找到需要更新的交易日
from datetime import date
tday=date.today()
tday_str=tday.strftime('%Y-%m-%d')

jdb=JuYuanDB()
tradingday=jdb.query_tradingday('2010-01-01',tday_str)
ind_last_tradingday=(tradingday['TradingDate']<tday_str)[::-1].idxmax()
last_tradingday=tradingday['TradingDate'].iloc[ind_last_tradingday]
last_tradingday_str=last_tradingday.strftime('%Y-%m-%d')
#%% 
fpath='D:/storedData/data_record.p'
record_p = Path(fpath)
update_window=30 # 用于更新的往前回推的window

if record_p.exists():
    record=pickle.load(open(fpath,'rb'))
    if record['update_tradingday']>=last_tradingday:
        pass
    else:
        update_startdate=tradingday['TradingDate'].iloc[ind_last_tradingday-update_window]  # 往前推30个交易日应该够了
        update_startdate_str=update_startdate.strftime('%Y-%m-%d')
else:
    update_startdate=datetime.date(2010, 1, 1)
    update_startdate_str=update_startdate.strftime('%Y-%m-%d')
#%% 更新daily数据
fpath_daily='D:/storedData/stockdailydata/'

#%% 更新收盘价
current_path=fpath_daily+'close.p'
if Path(current_path).exists():
    data.close






