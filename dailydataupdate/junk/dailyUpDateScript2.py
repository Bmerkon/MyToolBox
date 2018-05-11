# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:48:34 2017

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

#%%
from imp import reload
import dailyUpdate
reload(dailyUpdate)
from dailyUpdate.dailyUpDate import dailyUpDate
#%% 更新聚源数据库（直接整个读取即可）

du=dailyUpDate()
du.startDate='2010-01-01'
du.updateDate='2000-01-01'
#%%
t1=time.time()
data=du.dailyStockPrice()
t2=time.time()
print(t2-t1)
#%% 更新daily数据
fpath_daily='D:/storedData/stockdailydata/'

#%% 更新收盘价
name_dict=['PrevClosePrice', 'OpenPrice', 'HighPrice',
       'LowPrice', 'ClosePrice', 'TurnoverVolume', 'TurnoverValue',
       'TurnoverDeals']
for name in name_dict:    
    current_path=fpath_daily+name+'.p'
#if Path(current_path).exists():
    pickle.dump(data[['InnerCode','TradingDay',name]],open(current_path,'wb'))
    
    
#%% 更新复权因子
t1=time.time()
close=data[['InnerCode','TradingDay','ClosePrice']].copy()
close.columns=['innercode','info_publdate','ClosePrice']
close['data_date']=close['info_publdate']
restore=du.dailyRestore(close)
t2=time.time()
print(t2-t1)
#%%
current_path=fpath_daily+'restoref'+'.p'
pickle.dump(restore,open(current_path,'wb'))

#%%
