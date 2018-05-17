# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 10:07:15 2017

@author: Administrator
"""

factor_list=['tradingday','stockinfo','PrevClosePrice', 'OpenPrice', 'HighPrice',
       'LowPrice', 'ClosePrice', 'TurnoverVolume', 'TurnoverValue',
       'TurnoverDeals','restoref','restore_f_cum','close_r','ST','ST_list','notST_ind',
       'industry','industry_list','listed2now','ret','logret','Ashares','market_value',
       'indexcomp000300','indexcomp000905','indexcomp000016','DalutongHolding']

factor_params={}

factor_params['tradingday']={'class_name':'TradingDate','window':0,
             'params':{'first_day':'2010-01-01','last_day':None},
             'replace_old':True,
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['stockinfo']={'class_name':'StockInfo','window':0,
             'params':{},
             'replace_old':True,
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['ClosePrice']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'ClosePrice'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['OpenPrice']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'OpenPrice'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['HighPrice']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'HighPrice'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['LowPrice']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'LowPrice'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['PrevClosePrice']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'PrevClosePrice'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['TurnoverVolume']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'TurnoverVolume'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['TurnoverValue']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'TurnoverValue'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['TurnoverDeals']={'class_name':'StockQuote','window':0,
             'params':{'first_day':None,'last_day':None,'name':'TurnoverDeals'},
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['restoref']={'class_name':'RestoreFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'cum':False},
             'data_names_f':['stockinfo'],
             'replace_old':True,
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['restore_f_cum']={'class_name':'RestoreFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'cum':True},
             'replace_old':True,
             'data_names_f':['restoref'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['close_r']={'class_name':'StockDailyPrice','window':0,
             'params':{},
             'replace_old':True,
             'data_names_f':['restore_f_cum','ClosePrice'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['ST']={'class_name':'STFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'ST'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['ST_list']={'class_name':'STFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'ST_list'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['notST_ind']={'class_name':'STFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'notST_ind'},
             'replace_old':True,
             'data_names_f':['ST'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['industry']={'class_name':'IndustryFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'industry_num','level':'FirstIndustryName'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['industry_list']={'class_name':'IndustryFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'industry_list','level':'FirstIndustryName'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['listed2now']={'class_name':'Listed2Now','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'nday':None},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['ret']={'class_name':'Ret','window':0,
             'params':{'nday':1,'log':False},
             'replace_old':True,
             'data_names_f':['close_r'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['logret']={'class_name':'Ret','window':0,
             'params':{'nday':1,'log':True},
             'replace_old':True,
             'data_names_f':['close_r'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['Ashares']={'class_name':'CapitalFactor','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'name':'Ashares'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['market_value']={'class_name':'MarketValue','window':0,
             'params':{},
             'replace_old':True,
             'data_names_f':['Ashares','ClosePrice'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['indexcomp000300']={'class_name':'IndexComp','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'index':'000300'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['indexcomp000905']={'class_name':'IndexComp','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'index':'000905'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['indexcomp000016']={'class_name':'IndexComp','window':0,
             'params':{'first_day':'2010-01-01','last_day':None,'index':'000016'},
             'replace_old':True,
             'data_names_f':['stockinfo'],
             'saving_path':'D:/storedData/dailyfactordata/'}

factor_params['DalutongHolding']={'class_name':'DaluTongHolding','window':0,
             'params':{'datapath':'D:/OneDrive/pythonwork/Otherwork/20171207hugangtong/first/first/first/data/position_hkex.csv'},
             'replace_old':False,
             'data_names_f':[],
             'saving_path':'D:/storedData/dailyfactordata/'}
