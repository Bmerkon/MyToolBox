# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 16:26:07 2017

@author: Administrator
"""
#%%
from JuyuanQuery import JuYuanDB
import JuyuanQuery
from imp import reload
reload(JuyuanQuery)
#%%
JDB=JuYuanDB()

#%%

# 测试tradingdate
tradingdate=JDB.query_tradingday('2001-01-01','2017-01-01')
tradingdate.head(5)
#%%
# 测试stockinfo
stockinfo=JDB.query_stockinfo()
stockinfo.head(5)

#%%


s=JDB.query_singlequote('000001','closeprice','2017-01-01','2017-10-01')
print(s)




