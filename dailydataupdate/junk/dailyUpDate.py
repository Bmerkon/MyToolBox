# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 18:49:18 2017

@author: Administrator
"""
import pandas as pd 
import numpy as np
import pickle
import sys
sys.path.append('D:/OneDrive/pythonwork/MyToolBox/DataImport/')
from JuyuanQuery import JuYuanDB
from mdapiDB import MDApi
import time
#%%
def my_save(variable,name):
    fpath_daily='D:/storedData/stockdailydata/'
    pickle.dump(variable,open(fpath_daily+name+'.p','wb'))
    
def my_load(name):
    fpath_daily='D:/storedData/stockdailydata/'
    data=pickle.load(open(fpath_daily+name+'.p','rb'))
    return data

def load_names(names,code=None,first_day=None,last_day=None,tradingdate=None):
    if code is None:
        code=my_load('stockinfo')['SecuCode']
    
    now_tradingday=my_load('tradingday')
    if first_day is None:
        if tradingdate is None:
            first_day=now_tradingday.iloc[0].dt.strftime('%Y-%m-%d').values[0]
        else:
            first_day=tradingdate.iloc[0].strftime('%Y-%m-%d')
    
    if last_day is None:
        if tradingdate is None:
            last_day=now_tradingday.iloc[-1].dt.strftime('%Y-%m-%d').values[0]
        else:
            last_day=tradingdate.iloc[-1].strftime('%Y-%m-%d')
        
        
    data={}
    for name in names:
        load_data=my_load(name)
        if name in ['market_value','close_r','PrevClosePrice', 'OpenPrice', 'HighPrice',
                    'LowPrice', 'ClosePrice', 'TurnoverVolume', 'TurnoverValue',
                    'TurnoverDeals','restore_f','restore_f_cum','ret','listed2now','shares']:
            
            data[name]=load_data.loc[(load_data.index>=first_day)&(load_data.index<=last_day),code]
        elif name in ['stockinfo']:
            data[name]=load_data[load_data['SecuCode'].isin(code)]
        elif name in ['tradingday']:
            jdb=JuYuanDB()
            data[name]=jdb.query_tradingday(first_day,last_day)
        elif name in ['ST_data']:
            data['notST_ind']=load_data['notST_ind'].loc[(load_data['notST_ind'].index>=first_day)&(load_data['notST_ind'].index<=last_day),code]
            data['ST']=load_data['ST'].loc[(load_data['ST'].index>=first_day)&(load_data['ST'].index<=last_day),code]
            data['STdict']=load_data['STdict']
        elif name in ['industry_data']:
            data['industry']=load_data['industry_num'].loc[(load_data['industry_num'].index>=first_day)&(load_data['industry_num'].index<=last_day),code]
            data['industrydict']=load_data['industry_list']
        elif name in ['index_comp']:
            temp_index_comp={}
            for key in load_data:
                key_indexind=load_data[key]
                temp_index_comp[key]=key_indexind.loc[(key_indexind.index>=first_day)&(key_indexind.index<=last_day),code]
            data['index_comp']=temp_index_comp
    return data
    
def stockdaily(last_day):
    jdb=JuYuanDB()
    first_day='2010-01-01'

    # 读取每日股票信息
    stockinfo=jdb.query_stockinfo()
    stock_innercode=stockinfo.index.values
    stock_code=stockinfo['SecuCode']
    my_save(stockinfo,'stockinfo')
    
    
    # 读取每日交易日信息
    tradingday=jdb.query_tradingday(first_day,last_day)
    my_save(tradingday,'tradingday')
    
    # 读取收盘价信息
    name_dict=['PrevClosePrice', 'OpenPrice', 'HighPrice',
       'LowPrice', 'ClosePrice', 'TurnoverVolume', 'TurnoverValue',
       'TurnoverDeals'] 
    tradingday=tradingday['TradingDate']
    for name in name_dict:  

        data_old=load_names([name])
        old_fv=data_old[name].dropna(axis=0,how='all')
        
        last_day_old=old_fv.index[-1]
        if last_day_old<tradingday.iloc[-1]:
            new_startday=tradingday[tradingday[tradingday==last_day_old].index+1].iloc[0]
        else: # 如果旧数据足够新，则跳过这个factor计算
            continue
        
        if new_startday<tradingday.iloc[-1]:    
            start_day_str=new_startday.strftime('%Y-%m-%d')
            new_data=jdb.query_stockquote(stock_innercode, name, start_day_str, last_day, mode='mat')
            new_data.columns=stock_code
            
            data=pd.DataFrame(index=tradingday,columns=stock_code,data=np.nan)
            data.update(old_fv)
            data.update(new_data,overwrite=False)
        
            my_save(data,name)
    
    # 读取复权信息
    restoref=jdb.query_restoref(stock_innercode, first_day, last_day, mode='mat')
    restore_reverse=restoref.iloc[::-1]
    restore_reverse_cum=restore_reverse.cumprod()
    restore_f_cum=restore_reverse_cum.iloc[::-1]
    restoref.columns=stock_code
    restore_f_cum.columns=stock_code
    
    my_save(restore_f_cum,'restore_f_cum')
    my_save(restoref,'restore_f')
    
    # 读取ST
    ST,ST_list=jdb.query_ST(stock_innercode,first_day,last_day,mode='mat')
    ST.columns=stock_code
    notST_ind=ST==0
    ST_data={'ST':ST,'STdict':ST_list,'notST_ind':notST_ind}
    my_save(ST_data,'ST_data')
    
    # 读取行业情况
    industry,industry_list=jdb.query_industry(stock_innercode, 'FirstIndustryName', first_day, last_day,mode='mat')
    industry.columns=stock_code
        
    industry_data={'industry_num':industry,'industry_list':industry_list}
    my_save(industry_data,'industry_data')
    
    # 读取上市天数
    listed2now=jdb.query_listed2now(stock_innercode,first_day,last_day)
    listed2now.columns=stock_code
    my_save(listed2now,'listed2now')
    
    # 计算ret
    close=load_names(['ClosePrice'])
    close_r=close*restore_f_cum
    ret=close_r.pct_change(1)
    my_save(close_r,'close_r')
    my_save(ret,'ret')
    
    # 获取市值
    shares=jdb.query_capital(stock_innercode,'Ashares',first_day,last_day,mode='mat')
    shares.columns=stock_code
    market_value=close*shares
    my_save(market_value,'market_value')
    my_save(shares,'shares')
    
    # 获取成分股
    index_names={'000300.SH':3145,'000016.SH':46,'000905.SH':4978}
    index_comp={}
    for key in index_names:
        index_comp[key]=jdb.query_indexcomp(stock_innercode,index_names[key],first_day,last_day,mode='mat')
        index_comp[key].columns=stock_code
    my_save(index_comp,'index_comp')
    
    
    
def stockmin(last_day):
    flist=fileslist('D:\storedData\stockmindata')
    dates=[]
    for f in flist:
        dates.append(f[9:19])
    
    datedf=pd.DatetimeIndex(dates)
    last_d=datedf.max()+pd.Timedelta('1D')
    last_d_str=last_d.strftime('%Y-%m-%d')
    jdb=JuYuanDB()
    tradingday=jdb.query_tradingday(last_d_str,last_day)
    if not tradingday.empty:
        tradingday['next_day']=tradingday['TradingDate']+pd.Timedelta('1 days')
        tradingday['start']=tradingday['TradingDate'].dt.strftime('%Y-%m-%d')
        tradingday['end']=tradingday['next_day'].dt.strftime('%Y-%m-%d')
        md=MDApi()
        fpath='D:/storedData/stockmindata'
        for iday in range(tradingday.shape[0]):
            t1=time.time()
            data=md.query_stockmin(tradingday['start'][iday],tradingday['end'][iday])
            if not data.empty:
                fname='/'+'stock_min'+tradingday['start'][iday]+'.p'
                pickle.dump( data, open( fpath+fname, "wb" ))
                t2=time.time()
                t=t2-t1
                print(tradingday['start'][iday])
                print(t)
    
    
def fileslist(folder):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(folder) if isfile(join(folder, f))]
    return onlyfiles
    

        

    