# -*- coding: utf-8 -*-
"""
Created on Mon Dec  4 16:21:29 2017

@author: Administrator
"""

#%%
jdb=JuYuanDB()
data=load_names(['stockinfo','tradingday'])
data2=jdb.query_income(data['stockinfo'].index,'OperatingRevenue','2001-01-01','2017-12-05',indenddate='All',mode='tab')

#%%
s_v=data2.pivot_table(values='OperatingRevenue',index='data_date',columns='innercode',aggfunc='mean')
s_date=data2.pivot_table(values='info_publdate',index='data_date',columns='innercode',aggfunc='last')

#%%
tradingday=data['tradingday']['TradingDate']
code=data['stockinfo'].index
df=pd.DataFrame(index=tradingday,columns=code)
#%%
l=s_v.unstack().to_frame()
l.columns=['value']
l2=s_date.iloc[:,0:100].unstack().to_frame()
l2.columns=['update']
lall=pd.merge(l,l2,how='outer',left_index=True,right_index=True)


#l['update']=s_date.iloc[:,1000:1100].unstack()
l.reset_index(inplace=True)
l.dropna(inplace=True)
#%%
info_data=l[['innercode','update','value']].pivot_table(index='update',columns='innercode',values='value',aggfunc='last')
#%%
union_date=tradingday.append(info_data.index.to_series()).reset_index(drop=True).sort_values().unique()
final_mat=pd.DataFrame(index=union_date,columns=code)
final_mat.update(info_data)
final_mat.fillna(method='ffill',inplace=True)
final_mat=final_mat.loc[tradingday,:]
#%%
import core
reload(core)
from core import update_data
from core import reg_residual_pd
#%%
secucode=data['stockinfo']['SecuCode']
data_l=load_names(['ret','market_value'],code=secucode,tradingdate=tradingday)
data_beta=load_names_f(['BETA'],code=secucode,tradingdate=tradingday)

res=reg_residual_pd(data_l['ret'],data_beta['BETA'])
#%%
import dailyUpDate
reload(dailyUpDate)
from dailyUpDate import load_names

import factorUpDate
reload(factorUpDate)
from factorUpDate import load_names_f


#%%
import customfactor
reload(customfactor)

#%%

bf=customfactor.BETA(indexname='market')
bf.inputs['ret']=data_l['ret'].iloc[:500,:100]
bf.inputs['market_value']=data_l['market_value'].iloc[:500,:100]
bff=bf.compute_factor()

#%%
def tt(x,y):
    a=x+y
    b=x-y
    return a,b

a=pd.DataFrame(index=[1,2,3,4],columns=[5,6,7],data=np.arange(0,12).reshape(4,3))
z=a.apply(tt,y=1)

#%%
p={}
for j in range(len(z.iloc[0])):
    p[j]={}
    for i in z.index:
        p[j][i]=z[i][j]
    p[j]=pd.DataFrame(p[j])
        
