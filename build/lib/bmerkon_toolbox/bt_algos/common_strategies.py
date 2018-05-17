# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 20:43:12 2017

@author: Administrator
"""
import pandas as pd 
import numpy as np
import pickle
import pdb
import sys
import pyodbc as db_odbc
import psycopg2 as db_pgs

import time
import datetime
import alphalens

import bt
from bt.core import Algo
from imp import reload



#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/DataImport/')
#from JuyuanQuery import JuYuanDB
from bmerkon_toolbox.dbconnect.juyuan_DB import JuYuanDB

#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/dailydataupdate/dailyUpdate/')
#from dailyUpDate import load_names
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/factor/customfactor_p/')
#from customfactor.customfactor import load_names_f
#from customfactor import load_names_f
#from bmerkon_toolbox.dailydataupdate.dailyUpdate.factorUpDate import load_names_f
from bmerkon_toolbox.bt_algos import algos
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/bt_algos/')
#import algos
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/SimpleTools/')
#from basicfunctions import *
from bmerkon_toolbox.simple_tools.basic_functions import my_load,my_save
#from bmerkon_toolbox.SimpleTools.basicfunctions import *
#%%
def commission_fn(p,q):
    return np.abs(p*q*0.001)
#%%    
class factor_strategy:
    
    def __init__(self):
        self.quantile=5
        self.holding=10
        self.initial_capital=1000000
        self.offset=0
        self.descending=True
        
        self.factor_value=[]
        self.price=[]
        self.commission_fn=commission_fn
    
    def get_tester(self):
        st=bt.Strategy('factor',
              [
                  bt.algos.RunEveryNPeriods(self.holding,offset=self.offset),
                  algos.SetTemp(self.factor_value,'stat',dropna=False,empty_allowed=True),
                  bt.algos.SelectN(1/self.quantile,sort_descending=self.descending),
                  bt.algos.WeighEqually(),
                  bt.algos.Rebalance()
                  
              ]
                  )
        
        btester=bt.Backtest(st,self.price,initial_capital=self.initial_capital,commissions=self.commission_fn,progress_bar=True)
        return btester

#%%    
class longonly_strategy:
    
    def __init__(self):
        self.price=[]
        self.initial_capital=1000000
        
    def get_tester(self):
        st=bt.Strategy('long only',
                       [
                           bt.algos.RunOnce(),
                           bt.algos.SelectAll(),
                           bt.algos.WeighEqually(),
                           bt.algos.Rebalance()
                       ]
                           )
        
        btester=bt.Backtest(st,self.price,initial_capital=self.initial_capital,integer_positions=False,progress_bar=True)
        return btester
        
#%% 

class port_strategy:
    
    def __init__(self):
        self.holding=10
        self.offset=0
        self.initial_capital=1000000
        
        self.alpha_return=[]
        self.price=[]
        self.style_factor=None
        self.bench_weights=None
        self.optimizer=[]
        self.commission_fn=commission_fn
    
    def get_tester(self):
        st=bt.Strategy('port',
              [
                  bt.algos.RunEveryNPeriods(self.holding,offset=self.offset),
                  algos.OptWeights(self.optimizer,self.alpha_return,self.bench_weights,self.style_factor),
                  bt.algos.Rebalance()   
              ]
                  )
        
        btester=bt.Backtest(st,self.price,initial_capital=self.initial_capital,commissions=self.commission_fn,progress_bar=True)
        return btester
    
#%%
class by_weights_strategy:
    
    def __init__(self):
        self.weights_df=None
        self.initial_capital=1000000
        self.price=[]
        self.commission_fn=commission_fn
        
    def get_tester(self):
        
        st=bt.Strategy('strategy',
              [
                  algos.RunOnDate(self.weights_df.index),
                  algos.SetTemp(self.weights_df,'weights'),
                  bt.algos.Rebalance()   
              ]
                  )
        
        btester=bt.Backtest(st,self.price,initial_capital=self.initial_capital,commissions=self.commission_fn,progress_bar=True)
        return btester
        
    
#%%
class by_weights_strategy2:
    
    def __init__(self):
        self.weights_df=None
        self.initial_capital=1000000
        self.price=[]
        self.commission_fn=commission_fn
        self.buy_not_allowed=None
        self.sell_not_allowed=None
        
    def get_tester(self):
        
        st=bt.Strategy('strategy',
              [     
                  algos.SetTemp(self.buy_not_allowed,'buy_not_allowed'),
                  algos.SetTemp(self.sell_not_allowed,'sell_not_allowed'),
                  algos.DealClose(),    
                  algos.RunOnDate(self.weights_df.index),
                  algos.SetTemp(self.weights_df,'weights'),
                  algos.RebalanceBuySellAllowed()   
              ]
                  )
        
        btester=bt.Backtest(st,self.price,initial_capital=self.initial_capital,commissions=self.commission_fn,progress_bar=True)
        return btester  