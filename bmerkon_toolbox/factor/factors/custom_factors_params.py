# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:10:59 2017

@author: Administrator
"""

factor_list=['LNCAP','BETA','BETA300', 'BETA50', 'BETA500','DASTD','CMRA','Q']

factor_params={}

factor_params['LNCAP']={'class_name':'LNCAP','window':0,
             'params':{},
             'data_names':['market_value'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['BETA300']={'class_name':'BETA','window':252,
             'params':{'indexname':'000300','window':252,'min_window':100,'half_life':63,'output':'beta'},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['BETA500']={'class_name':'BETA','window':252,
             'params':{'indexname':'000905','window':252,'min_window':100,'half_life':63,'output':'beta'},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['BETA50']={'class_name':'BETA','window':252,
             'params':{'indexname':'000016','window':252,'min_window':100,'half_life':63,'output':'beta'},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['BETA']={'class_name':'BETA','window':252,
             'params':{'indexname':'market','window':252,'min_window':100,'half_life':63,'output':'beta'},
             'data_names':['ret','market_value'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['RSTR']={'class_name':'RSTR','window':504,
             'params':{'window':504,'lag':21,'half_life':126},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['DASTD']={'class_name':'DASTD','window':252,
             'params':{'window':252,'half_life':42},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['CMRA']={'class_name':'CMRA','window':252,
             'params':{'window':252,'days_permonth':21,'num_month':12},
             'data_names':['ret'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['Q']={'class_name':'QFactor','window':10,
             'params':{'sratio':0.2,'vabandratio':0.2,'sday':10,'maxnumnan':500,'numminutesperday':240},
             'data_names':['restore_f_cum','tradingday'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['apm']={'class_name':'APMFactor','window':20,
             'params':{'maxnan_stat':10,'maxnonan_reg':100,'sday':20,'morning_end':119,'afternoon_start':120},
             'data_names':['close_r','tradingday'],
             'saving_path':'D:/storedData/dailyfactordata/'}
