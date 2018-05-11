# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 10:30:49 2017

@author: Administrator
"""

#%%
from dailyUpdate.dailyUpDate import dailyUpDate
du=dailyUpDate()
du.startDate='2010-01-01'
du.updateDate='2000-01-01'
data=du.dailyStockPrice()

#%%
import pickle
pickle.dump()