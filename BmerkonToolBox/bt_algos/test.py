# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 11:59:17 2017

@author: Administrator
"""

import bt
from bt.core import Algo
import pyfolio
from pyfolio import tears
import pandas as pd
import numpy as np
from imp import reload
import sys
sys.path.append('D:\pythonwork\MyToolBox\DataImport')
from JuyuanQuery import JuYuanDB
JDB=JuYuanDB()
reload(pyfolio)
reload(tears)


#%% 构造价格序列
data=pd.DataFrame({
    'p1':range(10),
    'p2':np.ones(10)
})
data['p1']=data['p1'].add(1)
# 构造日期
rng = pd.date_range('1/1/2011', periods=10, freq='D')
data.index=rng

data.iloc[5,1]=0.8
data

#%%
sys.path.append('D:/pythonwork/MyToolBox/bt_algos')
import algos

#%%
data2 = bt.get('aapl,msft', start='2010-01-01')
#%%
data3=data2.iloc[0:20,:]
data3.head()
sig=[1,-1,1,1,-1,1,1,-1,1,1,-1,-1,1,1,1,-1,-1,-1,1,1]
sigdata=pd.DataFrame(index=data3.index,data=np.array(sig),columns=['sig'])
sigdata['trade']=sigdata.diff()
sigdata.fillna(1)



#%%
reload(algos)
s0=bt.Strategy('ss',[
    bt.algos.SelectAll(),
    algos.tt(sigdata),
    algos.RebalanceByPosition()
])

backt1=bt.Backtest(s0,data3)
res1=backt1.run()