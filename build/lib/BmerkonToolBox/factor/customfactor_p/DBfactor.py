# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 21:44:21 2017

@author: Administrator
"""

import pandas as pd
import numpy as np
import pdb
from sklearn import linear_model
import statsmodels.api as sm
import sys
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/DataImport/')
from BmerkonToolBox.DataImport.JuyuanQuery import JuYuanDB
#from JuyuanQuery import JuYuanDB
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/dailydataupdate/dailyUpdate/')
#from dailyUpDate import load_names
#from factorUpDate import load_names_f
from BmerkonToolBox.dailydataupdate.dailyUpdate.factorUpDate import load_names_f
#import dailyUpDate
import pickle
#%%
#from core import custom_factor
#from core import computeWeights
#from core import apply_multi_returns
from BmerkonToolBox.factor.customfactor_p.core import custom_factor,computeWeights,apply_multi_returns

#%% factors 
class TradingDate(custom_factor):
    def __init__(self,first_day='2010-01-01',last_day='2010-01-01'):
        self.name='TradingDate'
        self.params['first_day']=first_day
        self.params['last_day']=last_day
    
    def compute_factor(self):
        jdb=JuYuanDB()
        tradingday=jdb.query_tradingday(self.params['first_day'],self.params['last_day'])
        tradingday['datestr']=tradingday['TradingDate'].dt.strftime('%Y-%m-%d')
        return tradingday
    
class StockInfo(custom_factor):
    def __init__(self):
        pass
    
    def compute_factor(self):
        jdb=JuYuanDB()
        stockinfo=jdb.query_stockinfo()
        return stockinfo
    
class StockQuote(custom_factor):
    def __init__(self,name,first_day='2010-01-01',last_day='2010-01-01'):
        self.params['name']=name
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        
    def compute_factor(self):
        stock_innercode=self.inputs['stockinfo'].index
        code=self.inputs['stockinfo']['SecuCode']
        name=self.params['name']
        
        jdb=JuYuanDB()
        #pdb.set_trace()
        quote=jdb.query_stockquote(stock_innercode, name, self.params['first_day'],self.params['last_day'], mode='mat')
        quote.columns=code
        return quote
    
class StockDailyPrice(custom_factor):
    def __init__self(self):
        pass
    
    def compute_factor(self):
        dailyprice=self.inputs['ClosePrice']*self.inputs['restore_f_cum']
        dailyprice=dailyprice.fillna(method='ffill')
        return dailyprice
        
    
class RestoreFactor(custom_factor):
    def __init__(self,first_day='2010-01-01',last_day='2010-01-01',cum=True):
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        self.params['cum']=cum
    
    def compute_factor(self):
        if self.params['cum']:
            #pdb.set_trace()
            restoref=self.inputs['restoref']
            restore_reverse=restoref.iloc[::-1]
            restore_reverse_cum=restore_reverse.cumprod()
            restore_f_cum=restore_reverse_cum.iloc[::-1]
            return restore_f_cum
        else:
            stock_innercode=self.inputs['stockinfo'].index
            code=self.inputs['stockinfo']['SecuCode']
                        
            jdb=JuYuanDB()
            restoref=jdb.query_restoref(stock_innercode, self.params['first_day'],self.params['last_day'], mode='mat')
            restoref.columns=code
            return restoref
        
class STFactor(custom_factor):
    def __init__(self,first_day='2010-01-01',last_day='2010-01-01',name='ST'):
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        self.params['name']=name
        
    def compute_factor(self):
        if self.params['name']=='notST_ind':
            notST_ind=self.inputs['ST']==0
            return notST_ind
        
        stock_innercode=self.inputs['stockinfo'].index
        code=self.inputs['stockinfo']['SecuCode']
                
        jdb=JuYuanDB()
        ST,ST_list=jdb.query_ST(stock_innercode,self.params['first_day'],self.params['last_day'],mode='mat')
        ST.columns=code
        if self.params['name']=='ST':
            return ST
        else:
            return ST_list
        
class IndustryFactor(custom_factor):
    def __init__(self,first_day='2010-01-01',last_day='2010-01-01',name='industry_num',level='FirstIndustryName'):
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        self.params['name']=name
        self.params['level']=level
        
    def compute_factor(self):
        
        stock_innercode=self.inputs['stockinfo'].index
        code=self.inputs['stockinfo']['SecuCode']
        
        jdb=JuYuanDB()
        industry,industry_list=jdb.query_industry(stock_innercode,self.params['level'],self.params['first_day'],self.params['last_day'],mode='mat')
        industry.columns=code
        if self.params['name']=='industry_num':
            return industry
        else:
            return industry_list
        
class Listed2Now(custom_factor):
    def __init__(self,first_day='2010-01-01',last_day='2010-01-01',nday=None):
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        self.params['nday']=nday

    def compute_factor(self):
        if self.params['nday'] is None:
            stock_innercode=self.inputs['stockinfo'].index
            code=self.inputs['stockinfo']['SecuCode']
                    
            jdb=JuYuanDB()
            listed2now=jdb.query_listed2now(stock_innercode,self.params['first_day'],self.params['last_day'])
            listed2now.columns=code
            return listed2now
        else:
            listed_quaind=self.inputs['listed2now']>self.params['nday']
            return listed_quaind
        
class Ret(custom_factor):
    def __init__(self,nday=1,log=False):
        self.params['nday']=nday
        self.params['log']=log

    def compute_factor(self):
        price=self.inputs['close_r']
        ret=price.pct_change(self.params['nday'])
        if self.params['log']:
            ret=ret.add(1).transform(np.log)
        return ret
    
class CapitalFactor(custom_factor):
    def __init__(self,name,first_day='2010-01-01',last_day='2010-01-01'):
        self.params['name']=name
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        
    def compute_factor(self):
        stock_innercode=self.inputs['stockinfo'].index
        code=self.inputs['stockinfo']['SecuCode']

        jdb=JuYuanDB()
        shares=jdb.query_capital(stock_innercode,self.params['name'],self.params['first_day'],self.params['last_day'],mode='mat')
        shares.columns=code
        return shares
    
class MarketValue(custom_factor):
    def __init__(self):
        pass
        
    def compute_factor(self):
        market_value=self.inputs['ClosePrice']*self.inputs['Ashares']
        market_value=market_value.fillna(method='ffill')
        return market_value
    
class IndexComp(custom_factor):
    def __init__(self,index,first_day='2010-01-01',last_day='2010-01-01'):
        self.params['index']=index
        self.params['first_day']=first_day
        self.params['last_day']=last_day
        
    def compute_factor(self):
        stock_innercode=self.inputs['stockinfo'].index
        code=self.inputs['stockinfo']['SecuCode']
        index_names={'000300':3145,'000016':46,'000905':4978}
        index_innercode=index_names[self.params['index']]
        
        jdb=JuYuanDB()
        index_comp=jdb.query_indexcomp(stock_innercode,index_innercode,self.params['first_day'],self.params['last_day'],mode='mat')
        index_comp.columns=code
        return index_comp
    
class DaluTongHolding(custom_factor):
    def __init__(self,datapath=None):
        if datapath is None:
            self.params['datapath']='D:/OneDrive/pythonwork/Otherwork/20171207hugangtong/first/first/first/data/position_hkex.csv'
        else:
            self.params['datapath']=datapath
        
    def compute_factor(self):
        data=pd.read_csv(self.params['datapath'])
        data['stockCode']=data['stockCode'].astype(str)
        data['SecuCode']=data['stockName'].str[-7:-1]
        data['holdingPosition']=data['holdingPosition'].astype(int)
        mytable=data.pivot_table(index='date',columns='SecuCode',values='holdingPosition',aggfunc='last')
        mytable.index=pd.to_datetime(mytable.index) 
        return mytable