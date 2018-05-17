# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:29:30 2017

@author: Administrator
"""

import pandas as pd
import numpy as np
import time
import pdb
#from imp import reload
#import sys
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/dailydataupdate/dailyUpdate/')
#from dailyUpDate import load_names
#import dailyUpDate
import pickle
from pathlib import Path
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/SimpleTools/')
from bmerkon_toolbox.simple_tools.basic_functions import my_save,my_load

#%%
def my_load_f(name):
    fpath_daily='D:/storedData/dailyfactordata/'
    data=my_load(fpath_daily+name+'.p')
    #data=pickle.load(open(fpath_daily+name+'.p','rb'))
    return data

def load_names_f(names,code=None,first_day=None,last_day=None,tradingdate=None):
    # 给定条件，载入算好的各类因子
    #pdb.set_trace()
    if code is None:
        code=my_load_f('stockinfo')['SecuCode']
    # 处理交易日
    now_tradingday=my_load_f('tradingday')
    if first_day is None:
        if tradingdate is None:
            first_day=now_tradingday['TradingDate'].iloc[0].strftime('%Y-%m-%d')
        else:
            first_day=tradingdate.iloc[0].strftime('%Y-%m-%d')
    
    if last_day is None:
        if tradingdate is None:
            last_day=now_tradingday['TradingDate'].iloc[-1].strftime('%Y-%m-%d')
        else:
            last_day=tradingdate.iloc[-1].strftime('%Y-%m-%d')
  
    data={}
    # 载入数据
    for name in names:
        load_data=my_load_f(name)
        if name in ['tradingday']:
            data[name]=load_data[(load_data['TradingDate']>=first_day)&(load_data['TradingDate']<=last_day)]
        elif name in ['stockinfo']:
            data[name]=load_data[load_data['SecuCode'].isin(code)]    
        elif name in ['industry_list','ST_list']:
            data[name]=load_data
        else:
            data[name]=load_data.loc[(load_data.index>=first_day)&(load_data.index<=last_day),code]
    
    return data

#%%


def update_factors(factor_list,factor_params,customfactor,last_day,init=False,new_start_str=None):
    #pdb.set_trace()
    factor_list=factor_list.copy()
    factor_params=factor_params.copy()
    
    data=load_names_f(['tradingday','stockinfo'],first_day='2010-01-01',last_day=last_day)
    code=data['stockinfo']['SecuCode']
    tradingday=data['tradingday']['TradingDate']
    
    
    if new_start_str is not None:
        new_start_s=tradingday[tradingday>=new_start_str]
        if new_start_s.empty:
            return
        else:
            new_start=new_start_s.iloc[0]
            new_start_str=new_start.strftime('%Y-%m-%d')
    else:
        new_start=None
    # 按顺序更新
    for fname in factor_list:
        # 1. 初始化
        t1=time.time()
        print(fname)
        # 2. 找到path
        fullpath=factor_params[fname]['saving_path']+fname+'.p'
        
        # 3. 特殊情况，每日直接生成即可
        #pdb.set_trace()
        if ('replace_old' in factor_params[fname]) and factor_params[fname]['replace_old']:
            # 8. 初始化因子计算类
            new_f=eval('customfactor.'+factor_params[fname]['class_name']+'(**factor_params[fname][\'params\'])')
            
            if 'data_names' in factor_params[fname]:
                data=load_names_f(factor_params[fname]['data_names'])
            # 9. 带入参数
                for idata in factor_params[fname]['data_names']:
                    new_f.inputs[idata]=data[idata]
            #pdb.set_trace()
            if 'data_names_f' in factor_params[fname]:
                data=load_names_f(factor_params[fname]['data_names_f'])
            # 9. 带入参数
                for idata in factor_params[fname]['data_names_f']:
                    new_f.inputs[idata]=data[idata]
            # 10. 因子值计算
            new_fv=new_f.compute_factor()
            my_save(new_fv,fullpath)
            t2=time.time()
            print(t2-t1)
            continue
            
        
        # 3. 如果第一次生成，那么首先初始化
        if (not Path(fullpath).is_file()) or init==True:
            fvalue=pd.DataFrame()
            my_save(fvalue,fullpath)

        # 4. 载入旧数据
        old_fv=my_load(fullpath)
        # 5. 获得new_startday，即新数据计算开始日期
        if old_fv.empty:# 为空，则从tradingday的第一天开始算起
            if new_start is None:# 如果不指定默认更新时间
                new_startday=tradingday.iloc[0]
            else:
                new_startday=new_start
        else:# 非空的话，根据旧数据的最后一天，经过window调整
            old_last_day=old_fv.index[-1]
            if new_start is not None:
                new_startday=new_start
            elif old_last_day<tradingday.iloc[-1]:
                #pdb.set_trace()
                update_index=(tradingday[tradingday==old_last_day].index+1-factor_params[fname]['window'])[0]
                
                new_startday_max=tradingday[max(0,update_index)]
                    
                if new_start is None:# 如果不指定默认更新时间
                    new_startday=new_startday_max
                else:
                    new_startday=min(new_start,new_startday_max)
            else: # 如果旧数据足够新，则跳过这个factor计算
                continue
        
        if ('first_day' in factor_params[fname]['params']) and (factor_params[fname]['params']['first_day'] is None):
            factor_params[fname]['params']['first_day']=new_startday.strftime('%Y-%m-%d')
        #pdb.set_trace()    
        # 6.调用factor计算方法更新数据  
        
        if new_startday<=tradingday.iloc[-1]:
            #new_startday_str=new_startday.strftime('%Y-%m-%d')
            
            
            # 8. 初始化因子计算类
            new_f=eval('customfactor.'+factor_params[fname]['class_name']+'(**factor_params[fname][\'params\'])')
            # 7. 载入因子计算所用原始数据
            if 'data_names' in factor_params[fname]:
                data=load_names_f(factor_params[fname]['data_names'],first_day=new_startday,last_day=last_day)
            # 9. 带入参数
                for idata in factor_params[fname]['data_names']:
                    new_f.inputs[idata]=data[idata]
            #pdb.set_trace()
            if 'data_names_f' in factor_params[fname]:
                data=load_names_f(factor_params[fname]['data_names_f'],first_day=new_startday,last_day=last_day)
            # 9. 带入参数
                for idata in factor_params[fname]['data_names_f']:
                    new_f.inputs[idata]=data[idata]
            
            # 10. 因子值计算
            new_fv=new_f.compute_factor()
            
            # 11. 存储
            all_fv=pd.DataFrame(index=tradingday,columns=code,data=np.nan)
            all_fv.update(old_fv)
            all_fv.update(new_fv[new_fv.index>=new_startday],overwrite=True)
            my_save(all_fv,fullpath)
        t2=time.time()
        print(t2-t1)
        
