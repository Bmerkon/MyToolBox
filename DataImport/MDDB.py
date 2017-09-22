import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import datetime
import pdb

class MDDB:
    def __init__(self):
        self.conn = db_pgs.connect(database='mdserver',user='mdapi',password='mdapi',host='192.168.1.190',port='5432')
        self.sql_fpath = 'D:\pythonwork\MyToolBox\DataImport\privatefunctions'
        self.firstday = '2010-01-01'
        self.lastday = '2017-06-01'

    def file2query(self, filename):
        f = open((self.sql_fpath + '\\' + filename))
        sql = f.read()
        return sql

    def query_stockquote(self,name,first_day,last_day):
        sql = self.file2query('tradingday.sql')
        tradingdate = pd.read_sql(sql, self.conn, params=[first_day, last_day])
        return tradingdate

