# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 14:40:17 2017

@author: Administrator
"""
import pandas as pd
import numpy as np
import sys
#sys.path.append('D:/OneDrive/pythonwork/MyToolBox/dailydataupdate/dailyUpdate/')
#from dailyUpDate import load_names
sys.path.append('D:/OneDrive/pythonwork/MyToolBox/factor/customfactor_p/')
#from customfactor.customfactor import load_names_f
from customfactor import load_names_f
import pdb

#%%
def computeWeights(nday,half_life):
    # 最后一个权重最大！
    # 计算半衰参数
    delta=0.5**(1/half_life)
    weights=np.empty(nday)
    weights[:]=np.nan
    for i in range(nday):
        weights[i]=(1-delta)*delta**i
    return weights

def standardize_barra(factor):
    code=factor.columns
    tradingday=factor.index
    market_v=load_names_f(['market_value'],code=code,tradingdate=tradingday)
    #pdb.set_trace()
    factor_T=factor.T
    market_v_T=market_v['market_value'].fillna(method='ffill').T
    weights=market_v_T/market_v_T.sum()
    weighted_mean=(factor_T*weights).sum()
    f_std=(factor_T-weighted_mean).std()
    
    factor_barra=((factor_T-weighted_mean)/f_std).T
    return factor_barra
    
def clean_factor(tradingdate,code,factor_v):
    new_f=pd.DataFrame(index=tradingdate,columns=code,data=np.nan)
    new_f=new_f.update(factor_v)
    
    return new_f 

from sklearn import linear_model
def reg_residual(X,y):
    mdl=linear_model.LinearRegression()
    mdl.fit(X,y)
    residual=y-mdl.predict(X)
    return residual

def reg_column(y,X):
    #pdb.set_trace()
    residual_s=pd.Series(index=y.index)
    date=y.name
    if type(X)==pd.core.frame.DataFrame:
        if date in X.index:
            X_data=X.loc[date,:].to_frame()
        else:
            return residual_s
    elif type(X)==pd.core.panel.Panel:
        if date in X.iloc[0].index:
            X_data=X[:][:][date].T
        else:
            return residual_s
        
    X_nonan=X_data.dropna().index
    y_nonan=y.dropna().index
    index_nonan=X_nonan.intersection(y_nonan)
    
    
    if len(index_nonan)>1:
        #pdb.set_trace()
        residual=reg_residual(X_data.loc[index_nonan,:].values,y[index_nonan].values)
        residual_s[index_nonan]=residual
    return residual_s

def reg_residual_pd(Y_df,X_panel):
    Y_df_T=Y_df.T
    residual=Y_df_T.apply(reg_column,X=X_panel).T
    return residual
    
def apply_multi_returns(data,name_list):
    df_dict={}
    for j in range(len(data.iloc[0])):
        name_j=name_list[j]
        df_dict[name_j]={}
        for i in data.index:
            df_dict[name_j][i]=data[i][j]
        df_dict[name_j]=pd.DataFrame(df_dict[name_j])
    return df_dict

def update_data(code,tradingday,data_value,data_update,ffill=True):
    tab_v=data_value.unstack().to_frame()
    tab_v.columns=['value']
    tab_d=data_update.unstack().to_frame()
    tab_d.columns=['update']
    tab=pd.merge(tab_d,tab_v,how='outer',left_index=True,right_index=True)
    
    tab.reset_index(inplace=True)
    tab.dropna(inplace=True)
    tab['innercode']=tab.index.get_level_values(1)
    info_data=tab[['innercode','update','value']].pivot_table(index='update',columns='innercode',values='value',aggfunc='last')
    
    union_date=tradingday.append(info_data.index.to_series()).reset_index(drop=True).sort_values().unique()
    final_mat=pd.DataFrame(index=union_date,columns=code)
    final_mat.update(info_data)
    if ffill:
        final_mat.fillna(method='ffill',inplace=True)
    final_mat=final_mat.loc[tradingday,:]
    return final_mat
    

class custom_factor:
    
    name='custom_factor'
  
    inputs={}
    params={}
        
    def __init__(self):
        pass
    
    def compute_factor(self):
        
        pass
    