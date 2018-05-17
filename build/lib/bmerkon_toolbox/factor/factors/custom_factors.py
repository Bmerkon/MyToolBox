# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:42:42 2017

@author: Administrator
"""

import pandas as pd
import numpy as np
import pdb
from sklearn import linear_model
import statsmodels.api as sm
import sys

from bmerkon_toolbox.dbconnect.juyuan_DB import JuYuanDB
from pathlib import Path
import time

import pickle
#%%
from bmerkon_toolbox.factor.core import CustomFactor,compute_weights,apply_multi_returns

#%% factors    
class LNCAP(CustomFactor):
    
    def __init__(self):
        self.name='LNCAP'

        
    def compute_factor(self):
        mktv=self.inputs['market_value'].fillna(method='ffill').astype(float).T
        ln_mktv=mktv.transform(np.log)
        factor_v=(ln_mktv-ln_mktv.mean())/ln_mktv.std()
        return factor_v.T
        
class BETA(CustomFactor):
    
    def __init__(self,indexname='000300',window=252,min_window=100,half_life=63,output='beta'):
        self.name='BETA'
        self.params['indexname']=indexname
        self.params['window']=window
        self.params['min_window']=min_window
        self.params['half_life']=half_life
        self.params['output']=output
        
    def compute_factor(self):
        ret=self.inputs['ret']
       
        weights=compute_weights(self.params['window'],self.params['half_life'])
        weights=np.flipud(weights)
        
        date_index=ret.index.values
        
        if self.params['indexname']=='market':
            market_v_T=self.inputs['market_value'].fillna(method='ffill').T
            weights_market=(market_v_T/market_v_T.sum()).T
            
            indexret=(self.inputs['ret']*weights_market).sum(axis=1).values
        else:
            jdb=JuYuanDB()
            indexp=jdb.query_singlequote(self.params['indexname'],'closeprice',
                                         first_day=ret.index[0].strftime('%Y-%m-%d'),
                                         last_day=ret.index[-1].strftime('%Y-%m-%d'),type='index')
            
            indexret=indexp.pct_change().values
        
        
        #pdb.set_trace()
        data=ret.apply(BETA.rolling_beta,X=indexret,weights=weights,date_index=date_index,
                       window=self.params['window'],min_window=self.params['min_window'],output=self.params['output'])

        #pdb.set_trace()
        #data=apply_multi_returns(data,['beta','alpha','resid'])
        return data
        
    @staticmethod
    def rolling_beta(y,X,weights,date_index,window=252,min_window=100,output='beta'):

        #pdb.set_trace()
        # 检查数据维度是否符合
        assert len(X)==len(y)
    
        # 初始化数据
        ndate=y.shape[0]
        out_beta = np.empty(ndate)
        out_beta[:]=np.nan
        out_alpha=out_beta.copy()
        out_resid=out_beta.copy()
    
        # 找出股票的nan数据，并集算最近window天中有多少非nan数据
        indnull=y.isnull()
        indok=(~indnull).rolling(window).sum()
        
        # 设置成values便于计算
        indok_values=indok.values
        y_values=y.values
        
        # 给X（市场收益率）添加常数项1
        X_c=sm.add_constant(X)
    
        for iStart in range(0, len(X)-window):    
            # 确定window范围
            iEnd = iStart+window
            
            if indok_values[iEnd]>min_window: # 仅当有大于min_window个数的非nan数据时进行计算
                # 对应数据values
                Xi=X_c[iStart:iEnd]
                Yi=y_values[iStart:iEnd]
                # 找出非nan数据的ind
                indnani=np.isnan(Yi)
                # 进行WLS回归
                mdl=sm.WLS( Yi[~indnani],Xi[~indnani],weights[~indnani]).fit()
                
                 
                # 数据存储
                #out_dates.append(date_index[iEnd])
                out_beta[iEnd]=mdl.params[1]
                out_alpha[iEnd]=mdl.params[0]
                #pdb.set_trace()
                if not indnani[-1]:
                    #pdb.set_trace()
                    out_resid[iEnd]=mdl.resid[-1]
                
        #pdb.set_trace()
        if output=='beta':
            return out_beta
        elif output=='alpha':
            return out_alpha
        elif output=='resid':
            return out_resid  
        #return out_beta
        
class RSTR(CustomFactor):
    
    def __init__(self,window=504,lag=21,half_life=126):
        self.name='RSTR'
        self.params['window']=window
        self.params['lag']=lag
        self.params['half_life']=half_life  
        
    def compute_factor(self):
        
        log_ret=self.inputs['ret'].transform(lambda x:np.log(1+x))
        log_ret.shift(self.params['lag']).ewm(halflife=self.params['half_life']).mean()
        return log_ret
    
class DASTD(CustomFactor):
    def __init__(self,window=252,half_life=42):
        self.name='DASTD'
        self.params['window']=window
        self.params['half_life']=half_life 
        
    def compute_factor(self):
        dastd=self.inputs['ret'].ewm(halflife=self.params['half_life']).std()
        return dastd
    
class CMRA(CustomFactor):
    def __init__(self,window=252,num_month=12,days_permonth=21):
        self.name='CMRA'
        self.params['window']=window
        self.params['num_month']=num_month 
        self.params['days_permonth']=days_permonth 
        
    def compute_factor(self):
        
        ret=self.inputs['ret']
        ret_month=ret.fillna(0).transform(lambda x:np.log(1+x)).rolling(window=self.params['days_permonth']).sum()
        Zmax_T=ret_month.rolling(window=self.params['num_month']*self.params['days_permonth']).max()
        Zmin_T=ret_month.rolling(window=self.params['num_month']*self.params['days_permonth']).min()
        cmra=Zmax_T.add(1)/Zmin_T.add(1)
        return cmra
    
class HSIGMA(CustomFactor):
    def __init__(self,window=252,half_life=63):
        self.name='HSIGMA'
        self.params['window']=window
        self.params['half_life']=half_life 
        
    def compute_factor(self):
        
        
        return None
    

class NLSIZE(CustomFactor):
    def __init__(self,window=0):
        self.name='NLSIZE'
        self.params['window']=window
        
    def compute_factor(self):
        logmkt=self.inputs['LNCAP']
        # 待补充
        
class BTOP(CustomFactor):
    def __init__(self,window=0):
        self.name='BTOP'
        self.params['window']=window
        
    def compute_factor(self):
        
        btop=self.inputs['equity']/self.inputs['market_value'].fillna(method='ffill')
        return btop
        
class STO(CustomFactor):
    def __init__(self,window=21):
        self.name='STO'
        self.params['window']=window
        
    def compute_factor(self):
        sto_daily=self.inputs['volume']/self.inputs['shares']
        sto=sto_daily.rolling.mean(window=self.params['window'])
        return sto
    
class QFactor(CustomFactor):
   
    def __init__(self,sratio=0.2,vabandratio=0.2,sday=10,maxnumnan=500,numminutesperday=240):
        self.params['sratio']=sratio
        self.params['vabandratio']=vabandratio
        self.params['sday']=sday
        self.params['maxnumnan']=maxnumnan
        self.params['numminutesperday']=numminutesperday
        #self.inputs['restoref']=[]
     
    def query_stockpvmin_mat(self,select_day):
        fpath='D:/storedData/stockpvmindatanew'
        fname='/'+'stockpv_min'+select_day+'.p'
        my_file = Path(fpath+fname)
        if my_file.exists():
            data=pickle.load(open(fpath+fname,'rb'))
            return data
        else:
            return None    
        
    def compute_factor(self):
        datai=self.query_stockpvmin_mat('2013-08-29')
        nstock=datai['close'].shape[1]
        
        tradingdate=self.inputs['tradingday']
        ndate=tradingdate.shape[0]
        
        restoref=self.inputs['restore_f_cum']
        datein=[]
        closecumi=np.empty((0,nstock))
        volumecumi=np.empty((0,nstock))
        scumi=np.empty((0,nstock))
        Q=np.empty((ndate,nstock))*np.nan
        code_min=datai['close'].columns
        #tradingday=pd.DataFrame(index=self.tradingdate,data=self.tradingdate.strftime('%Y-%m-%d'),columns=['datestr'])
        
        #pdb.set_trace()
        for i,select_day in enumerate(tradingdate['datestr']):
            datai=self.query_stockpvmin_mat(select_day)
    
            t1=time.time()
            if datai is not None:
                datein.append(select_day)
            else:
                continue
            
            #pdb.set_trace()
            closei=datai['close'][code_min]*restoref.loc[select_day,code_min]
            volumei=datai['volume'][code_min]/restoref.loc[select_day,code_min]
            si=abs(closei.diff()/(volumei**0.5))
            
            closecumi=np.concatenate((closecumi,closei.values))
            volumecumi=np.concatenate((volumecumi,volumei.values))
            scumi=np.concatenate((scumi,si.values))
            
            if len(datein)>self.params['sday']:
                 
                closecumi=closecumi[self.params['numminutesperday']:,:]
                volumecumi=volumecumi[self.params['numminutesperday']:,:]
                scumi=scumi[self.params['numminutesperday']:,:]
                
                datein=datein[1:]
            
            
            if len(datein)==self.params['sday']:
                #pdb.set_trace()
                numnan=np.sum(np.isnan(scumi),axis=0)
                for j in range(nstock):
                    if numnan[j]>self.params['maxnumnan']:
                        continue
                    else:
                        I=np.argsort(scumi[:,j])
                        I=np.flipud(I)[numnan[j]:]
                        sj=scumi[I,j]
                        pj=closecumi[I,j]
                        vj=volumecumi[I,j]
                        
                        nabandon=np.round(self.params['vabandratio']*sj.shape[0]).astype(int)
                        vI=np.argsort(vj)
                        sj=np.delete(sj,vI[:nabandon])
                        pj=np.delete(pj,vI[:nabandon])
                        vj=np.delete(vj,vI[:nabandon])
                    
                        cumvj=np.cumsum(vj)
                        smart_ind=np.argwhere(cumvj/cumvj[-1]>self.params['sratio'])[0][0]
                        vwap_smart=np.sum(pj[:smart_ind]*vj[:smart_ind])/cumvj[smart_ind]
                        vwap_all=np.sum(pj*vj)/cumvj[-1]
                        Q[i,j]=vwap_smart/vwap_all
                    
                t2=time.time()
                print(select_day)
                print(t2-t1) 
        
        #pdb.set_trace()
        Qdf=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=Q)
        #Qdf=pd.DataFrame(index=tradingdate['TradingDate'],columns=self.code)
        #Qdf.update(Qdf_origin)
        
        return Qdf
    
class APMFactor(CustomFactor):
       
    def __init__(self,sday=20,morning_end=119,afternoon_start=120,maxnan_stat=10,maxnonan_reg=100):
  
        self.params['sday']=sday
        self.params['morning_end']=morning_end
        self.params['afternoon_start']=afternoon_start
        self.params['maxnan_stat']=maxnan_stat
        self.params['maxnonan_reg']=maxnonan_reg
        self.computedata={}
        
    def query_stockpvmin_mat(self,select_day):
        fpath='D:/storedData/stockpvmindatanew'
        fname='/'+'stockpv_min'+select_day+'.p'
        my_file = Path(fpath+fname)
        if my_file.exists():
            data=pickle.load(open(fpath+fname,'rb'))
            return data
        else:
            return None 
        
    def compute_factor(self):
        # 获取分钟数据相关信息
        datai=self.query_stockpvmin_mat('2013-08-29') # 读取样本分钟数据
        nstock=datai['close'].shape[1] # 分钟数据包含股票数
        code_min=datai['close'].columns # 分钟数据对应code
        
        # 其他数据计算
        tradingdate=self.inputs['tradingday']
        ndate=tradingdate.shape[0]
        params=self.params # 参数
        
        
        #%% 获取每日morning\afternoon数据
        # 初始化
        #pdb.set_trace()
        morning_p1=np.empty((ndate,nstock))*np.nan
        morning_p2=np.empty((ndate,nstock))*np.nan
        afternoon_p1=np.empty((ndate,nstock))*np.nan
        afternoon_p2=np.empty((ndate,nstock))*np.nan
        # 数据读取
        for i,select_day in enumerate(tradingdate['datestr']):
            datai=self.query_stockpvmin_mat(select_day)
            morning_p1[i,:]=datai['close'].iloc[0,:]
            morning_p2[i,:]=datai['close'].iloc[params['morning_end'],:]
            afternoon_p1[i,:]=datai['close'].iloc[params['afternoon_start'],:]
            afternoon_p2[i,:]=datai['close'].iloc[-1,:]
        # 计算各股、市场上下午收益率
        r_morning=morning_p2/morning_p1-1
        r_afternoon=afternoon_p2/afternoon_p1-1
        R_morning=np.nanmean(r_morning,axis=1)
        R_afternoon=np.nanmean(r_afternoon,axis=1)
        
        #%% 统计上下午数据中的nan数量，回归用
        indnan=np.isnan(r_morning)|np.isnan(r_afternoon) # 上午或者下午为nan
        nnan=pd.DataFrame(data=indnan).rolling(window=params['sday']).sum().fillna(0).astype(int).values
        from sklearn import linear_model
        #%% 计算stat
        stat=np.empty((ndate,nstock))*np.nan
        for i in range(params['sday'],ndate+1):
            #pdb.set_trace()
            t1=time.time()
            irm=r_morning[i-params['sday']:i,:].copy() # 数据到i，但是实际上i-1
            ira=r_afternoon[i-params['sday']:i,:].copy() # 数据到i，但是实际上i-1
            ir=np.concatenate([irm,ira])
            #print(ir.shape)
            iRm=R_morning[i-params['sday']:i].copy()# 数据到i，但是实际上i-1
            iRa=R_afternoon[i-params['sday']:i].copy()# 数据到i，但是实际上i-1
            iR=np.concatenate([iRm,iRa]).reshape(-1,1)
            #print(iR.shape)
            indnani=indnan[i-params['sday']:i,:].copy()
            #print(i)
            for j in range(nstock):
                nnanij=nnan[i-1,j]
                if nnanij<params['maxnan_stat']:#这个数字随便定的，只要nan个数小于某个值，就进行stat计算
                    # 1. 回归
                    reg = linear_model.LinearRegression()
                    ind_nonanij=np.concatenate([~indnani[:,j],~indnani[:,j]])
                    #pdb.set_trace()
                    X=iR[ind_nonanij] # X为市场上下午收益率R
                    y=ir[ind_nonanij,j] # y为股票上下午收益率r
                    reg.fit(X,y) # 计算回归参数
                    epi=y-reg.predict(X) # 获取残值
                    #pdb.set_trace()
                    deltai=epi[:params['sday']-nnanij]-epi[params['sday']-nnanij:]# 计算delta
                    stat[i-1,j]=deltai.mean()/deltai.std()
            t2=time.time()
            print(tradingdate['datestr'][i-1])
            print(t2-t1)
        
        #%% 对因子、动量进行横截面回归
        Ret=self.inputs['close_r'][code_min].pct_change(params['sday']).values # 计算n日动量
        
        indnan_stat=np.isnan(stat)
        indnan_ret=np.isnan(Ret)
        ind_nonan=(~indnan_stat)&(~indnan_ret)
        num_nonan=ind_nonan.sum(axis=1)
        
        epi_mat=np.empty((ndate,nstock))*np.nan # 初始化
        
        for i in range(params['sday'],ndate):
            if num_nonan[i]>params['maxnonan_reg']: # 
                reg = linear_model.LinearRegression(fit_intercept=False)
                indi=ind_nonan[i,:]
                X=Ret[i,indi].reshape(-1,1)
                y=stat[i,indi]
                reg.fit(X,y)
                epi=y-reg.predict(X)
                epi_mat[i,indi]=epi
        #%% 整理数据
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=epi_mat)
        self.computedata['apm']=df
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=stat)
        self.computedata['stat']=df
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=morning_p1)
        self.computedata['morning_p1']=df
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=morning_p2)
        self.computedata['morning_p2']=df
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=afternoon_p1)
        self.computedata['afternoon_p1']=df
        df=pd.DataFrame(index=tradingdate['TradingDate'],columns=code_min,data=afternoon_p2)
        self.computedata['afternoon_p2']=df
               
        apm_df=self.computedata['apm']
        return apm_df