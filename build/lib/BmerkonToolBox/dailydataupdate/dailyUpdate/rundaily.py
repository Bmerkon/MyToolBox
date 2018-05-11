# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 11:49:41 2017

@author: Administrator
"""
#%%

#import dailyUpDate
#from dailyUpDate import stockmin,stockdaily
#reload(dailyUpDate)
#import factorUpDate
#reload(factorUpDate)
#from factorUpDate import factordaily
##%%
#today='2017-12-04'
##stockmin(today)
#stockdaily(today)


#%%
import sys
from imp import reload
#sys.path.append('D:/pythonwork/MyToolBox/dailydataupdate/dailyUpdate')
#import DBfactor_params
#reload(DBfactor_params)

from BmerkonToolBox.dailydataupdate.dailyUpdate import DBfactor_params,factorUpDate
from BmerkonToolBox.dailydataupdate.dailyUpdate.DBfactor_params import factor_list,factor_params
#from DBfactor_params import factor_list 
#from DBfactor_params import factor_params
#import factorUpDate
#reload(factorUpDate)
from BmerkonToolBox.dailydataupdate.dailyUpdate.factorUpDate import factordaily
#sys.path.append('D:/pythonwork/MyToolBox/factor/customfactor_p')
#import DBfactor
#reload(DBfactor)
from BmerkonToolBox.factor.customfactor_p import DBfactor
last_day='2018-05-11'
#%%
for ifactor in factor_params:
    if 'params' in factor_params[ifactor]:
        if ('last_day' in factor_params[ifactor]['params']) and (factor_params[ifactor]['params']['last_day'] is None):
            factor_params[ifactor]['params']['last_day']=last_day

#%%
factor_list_select=factor_list
#factordaily()
factordaily(factor_list_select,factor_params,DBfactor,last_day)
#%%
import sys
import factor_params
reload(factor_params)
from factor_params import factor_list 
from factor_params import factor_params
sys.path.append('D:/pythonwork/MyToolBox/factor/customfactor_p')
import customfactor
reload(customfactor)
import factorUpDate
reload(factorUpDate)
from factorUpDate import factordaily

factordaily(factor_list,factor_params,customfactor,last_day)




