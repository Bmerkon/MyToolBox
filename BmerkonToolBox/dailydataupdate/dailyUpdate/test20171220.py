# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 08:54:44 2017

@author: Administrator
"""

import scrapy
import os
#%%
os.system('scrapy runspider scraper.py')

#%%
#g_num=1000000000
#t_num=g_num*1000
#N=30
#H_gh=1200
#H=H_gh*g_num
#B=12.5
#S=86400
#D_g=1800
#D=D_g*g_num
#
#BTC_price=18107.62
#
#power=1200
#power_cost=0.1
#
#hard_warecost=2000
#
##%%
#totalincome=N*B*H*86400/(D*2**32)*BTC_price*0.93
#totalincome
#
##%%
#H_th=[13.5]


#%%
g_num=1000000000
t_num=g_num*1000
import itertools

def calincome(N,B,H,D,S,btc_price,rej_rate,pool_rate,power,power_cost,main_fee):
    coinnum=N*B*H*S/(D*2**32)*(1-rej_rate)*(1-pool_rate)
    totalincome=coinnum*btc_price
    fee=24*N*power/1000*power_cost+main_fee
    return totalincome,fee,coinnum
#%%
machine_set={'AntS9':[13.5,1500,2000],'Avalon741':[7.3,1150,2000],'E90+':[9,1305,1800]}
machine=['AntS9','Avalon741','E90+']
machinenum=[1]
Dgrow=1.247
Dset=np.power(Dgrow,list(range(0,24)))*1870
#%%
paraset=[]
for N,B,D,S,btc_price,rej_rate,pool_rate,machinenumi,power_cost,main_fee in itertools.product([30],[12.5],Dset,[86400],[100000],[0.01],[0.01],machinenum,[0.5],[0]):
    machinename=machine[machinenumi-1]
    item=machine_set[machinename]
    
    H=item[0]*t_num
    power=item[1]
    income,fee,coinnum=calincome(N,B,H,D*g_num,S,btc_price,rej_rate,pool_rate,power,power_cost,main_fee)

    
    para=[N,B,D,H,S,btc_price,rej_rate,pool_rate,machinenumi,power,power_cost,main_fee,income,fee,coinnum]
    
    paraset.append(para)
    
L=pd.DataFrame(np.array(paraset))
L.columns=['N','B','D','H','S','btc_price','rej_rate','pool_rate','machinenumi','power','power_cost','main_fee','income','fee','coinnum']
L['machinename']=np.nan
L['machinename'][L['machinenumi']==1]=machine[0]
L['machinename'][L['machinenumi']==2]=machine[1]
L['machinename'][L['machinenumi']==3]=machine[2]

#%%
totalincome,fee,coinnum=calincome(N,B,H,D,S,btc_price,rej_rate,pool_rate,power,power_cost,main_fee)