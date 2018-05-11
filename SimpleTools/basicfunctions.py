# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 19:16:52 2017

@author: Administrator
"""
import pickle
import numpy as np
#%%
def my_save(variable,filename,path=None):
    if path is None:
        filepath=filename
    else:
        filepath=path+'/'+filename
        
    f=open(filepath,'wb')
    pickle.dump(variable,f)
    f.close()
    
    
def my_load(path):
    f=open(path,'rb')
    data=pickle.load(f)
    f.close()
    return data

def computeWeights(nday,half_life):
    # 最后一个权重最大！
    # 计算半衰参数
    delta=0.5**(1/half_life)
    weights=np.empty(nday)
    weights[:]=np.nan
    for i in range(nday):
        weights[i]=(1-delta)*delta**i
    return weights