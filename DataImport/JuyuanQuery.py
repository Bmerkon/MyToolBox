import pyodbc as db_odbc
#import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import pdb

class JuYuanDB():
   
    def __init__(self):
        self.conn=db_odbc.connect('DSN=JuYuan;UID=JYUSER;PWD=jyuser123456')
        self.sql_fpath='D:\pythonwork\MyToolBox\DataImport\privatefunctions'
        self.firstday='2010-01-01'
        self.lastday='2017-06-01'
    
    def file2query(self,filename):
        f=open((self.sql_fpath+'\\'+filename))
        sql=f.read()
        return sql
    
    # tradingday移植
    def query_tradingday(self,firstday,lastday):
        sql=self.file2query('tradingday.sql')
        tradingdate=pd.read_sql(sql,self.conn,params=[firstday,lastday])
        return tradingdate

    # stockinfo移植
    def query_stockinfo(self):
        sql=self.file2query('ashareList.sql')
        return pd.read_sql(sql,self.conn,index_col='InnerCode')
    
    # balancesheet
    def query_balance(self,stock_innercode,name,firstday,lastday,indenddate='All'):
        #pdb.set_trace()
        sql=self.file2query('ashareBalance.sql')
        print(name)
        sql=sql.replace('MySelected',name)
        if str(indenddate).capitalize()=='All':
            sql=sql.replace('and month(s.enddate)=?','')
            balance=pd.read_sql(sql,self.conn)
        else:
            balance=pd.read_sql(sql,self.conn,params=[indenddate])
            
        tradingdate=self.query_tradingday(firstday,lastday)
        balance['info_enddate']=self.find_end(balance['innercode'].values,balance['InfoPublDate'].values,tradingdate.iloc[-1])

        balance_mat=self.data2mat(stock_innercode,tradingdate,balance['innercode'],balance['InfoPublDate'],balance['info_enddate'],
           balance['enddate'],balance[name])
        pdb.set_trace()
        return balance_mat    
        #return balance
    
    def  find_end(self,s1,s2,last_s2):
        l=np.diff(s1)
        k=l!=0
        l=np.append(k,np.array([False]))
        sfinal=s2
        sfinal[l]=last_s2
        return sfinal
        
    
    def  data2mat(self,innercode_list,tradingdate,innercode,startdate,enddate,datadate,data):
        pdb.set_trace()
        ndata=len(innercode)
        ndate=len(tradingdate)
        nstock=len(innercode_list)
        ind_notdrop=np.array([True]*ndata)
        innercode_list=innercode_list.astype(int)
        code_list=innercode.unique()
        for code in code_list:
            indcode=innercode==code
            cummaxdate=pd.Series.cummax(datadate[indcode])
            ind_notdrop[indcode]=datadate[indcode]>=cummaxdate
            
        innercode_array=innercode.values[ind_notdrop]
        startdate_array=startdate.values[ind_notdrop]
        enddate_array=enddate.values[ind_notdrop]
        data_array=data.values[ind_notdrop]
        tradingdate_array=tradingdate.values
        ndata=len(innercode_array)
        result_tab=np.ones([ndate,nstock])*np.nan
        #tradingdate = pd.Series(list(map(pd.Timestamp, tradingdate) ))
        for index in range(ndata):
            #print ("row[startdate] = ", row['startdate'] , " type is ", type(row['startdate']))
            #print ("tradingdate = ", tradingdate, ", tpe is", type(tradingdate[0]))        
            ind_date=np.nonzero((tradingdate_array>=startdate_array[index]) &( tradingdate_array<=enddate_array[index]))[0]
            ind_stock=np.nonzero(innercode_list==innercode_array[index])[0]
            #pdb.set_trace()
            if (len(ind_date)>0) & (len(ind_stock)>0):
                result_tab[ind_date,ind_stock]=data_array[index]
        pdb.set_trace()    
        result_tab=pd.DataFrame(index=tradingdate,columns=innercode_list,data=result_tab)
        
        return result_tab

 #%%
#from JuyuanQuery import JuYuanDB



