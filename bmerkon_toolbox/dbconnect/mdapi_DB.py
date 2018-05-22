# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 08:37:51 2017

@author: Administrator
"""

import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import datetime
import pdb
import os


class MDApi:
    # 连接MDAPI的接口
    
    def __init__(self):
        self.conn=db_pgs.connect(database='mdserver',user='mdapi',password='mdapi',host='192.168.1.190',port='5432')
        self.sql_fpath =  os.path.dirname(os.path.abspath(__file__))+'/mdapi_sql'
        
    def file2query(self, filename):
        f = open((self.sql_fpath + '\\' + filename))
        sql = f.read()
        return sql
        
    def query_stockmin(self,first_day,last_day):
        
        sql=self.file2query('stockmin_MD.sql')
        data=pd.read_sql(sql,self.conn,params={'t1':first_day,'t2':last_day})
        if not data.empty:
            data=data.set_index('datetime')
            data.index=data.index.tz_convert('Hongkong')
        return data
    

class ChiApi:
    # 连接ChiAPI的接口
    def __init__(self):
        self.conn=db_pgs.connect(database='stockdata',user='gaoyuan',password='gaoyuan',host='192.168.1.20',port='5432')
        self.sql_fpath =  os.path.dirname(os.path.abspath(__file__))+'/mdapi_sql'
        
    def file2query(self, filename):
        f = open((self.sql_fpath + '\\' + filename))
        sql = f.read()
        return sql
        
    def query_stockmin(self,first_day,last_day):
        
        sql=self.file2query('stockmin_Chi.sql')
        data=pd.read_sql(sql,self.conn,params={'t1':first_day,'t2':last_day})
        if not data.empty:
            data=data.set_index('datetime')
            data.index=data.index.tz_localize('Hongkong')
        return data
