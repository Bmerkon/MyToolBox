# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 18:44:52 2017

@author: Administrator
"""

#%%
#fname='BETA'
#fvalue=pd.DataFrame()
#fullpath=fpath+'/'+fname+'.p'
#my_save(fvalue,fullpath)

#%%
sys.path.append('D:/OneDrive/pythonwork/MyToolBox/factor/')
import customfactor
reload(customfactor)


update_today='2017-02-28'
data=load_names(['tradingday','stockinfo'],first_day='2010-01-01',last_day=update_today)
code=data['stockinfo']['SecuCode']
tradingday=data['tradingday']['TradingDate']

for fname in factor_list:
    t1=time.time()
    print(fname)
    fullpath=factor_params[fname]['saving_path']+fname+'.p'
    
    
    
    old_fv=my_load(fullpath)
    if old_fv.empty:
        new_startday=tradingday.iloc[0]
    else:
        last_day=old_fv.index[-1]
        if last_day<tradingday.iloc[-1]:
            new_startday=tradingday[tradingday[tradingday==last_day].index+1-factor_params[fname]['window']].iloc[0]
        else:
            continue
        
    if new_startday<tradingday.iloc[-1]:
        new_startday_str=new_startday.strftime('%Y-%m-%d')
        data=load_names(factor_params[fname]['data_names'],first_day=new_startday,last_day=update_today)
        
        new_f=eval('customfactor.'+factor_params[fname]['class_name']+'(**factor_params[fname][\'params\'])')
        new_f.code=code
        for idata in factor_params[fname]['data_names']:
            new_f.inputs[idata]=data[idata]
        new_fv=new_f.compute_factor()
        
        all_fv=pd.DataFrame(index=tradingday,columns=code,data=np.nan)
        all_fv.update(old_fv)
        all_fv.update(new_fv,overwrite=False)
        my_save(all_fv,fullpath)
    t2=time.time()
    print(t2-t1)
