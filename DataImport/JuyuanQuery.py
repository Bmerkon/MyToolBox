import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import pdb


# 旧的

class JuYuanDB:
    def __init__(self):
        self.conn = db_odbc.connect('DSN=JuYuan;UID=JYUSER;PWD=jyuser123456')
        self.sql_fpath = 'D:\pythonwork\MyToolBox\DataImport\privatefunctions'
        self.firstday = '2010-01-01'
        self.lastday = '2017-06-01'

    def file2query(self, filename):
        f = open((self.sql_fpath + '\\' + filename))
        sql = f.read()
        return sql

    # tradingday移植
    def query_tradingday(self, firstday, lastday):
        sql = self.file2query('tradingday.sql')
        tradingdate = pd.read_sql(sql, self.conn, params=[firstday, lastday])
        return tradingdate

    # stockinfo移植
    def query_stockinfo(self):
        sql = self.file2query('ashareList.sql')
        return pd.read_sql(sql, self.conn, index_col='InnerCode')

    # balancesheet
    def query_balance(self, stock_innercode, name, firstday, lastday, indenddate='All'):

        sql = self.file2query('ashareBalance.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            balance = pd.read_sql(sql, self.conn)
        else:
            balance = pd.read_sql(sql, self.conn, params=[indenddate])

        tradingdate = self.query_tradingday(firstday, lastday)
        balance['info_enddate'] = self.find_end(balance['innercode'], balance['InfoPublDate'], tradingdate.iloc[-1])

        # pdb.set_trace()
        balance_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'], balance['innercode'],
                                    balance['InfoPublDate'], balance['info_enddate'],
                                    balance['enddate'], balance[name])
        # print(stock_innercode)
        # print(tradingdate)
        # print(balance['innercode'])
        # print(balance['InfoPublDate'])
        # print(balance['info_enddate'])
        # print(balance['enddate'])
        # print(balance[name])
        # pdb.set_trace()
        return balance_mat
        # return balance

    def find_end(self, code, start_date, last_end_date):
        # 这个函数用来解决为数据添加enddate的。比如我有股票和对应公告日，那每个股票的公告日有效期应该是该股票下个公告日之前，所以enddate就是该股票下个公告日。
        # 最后一次公告日使用last_end_day作为公告日结束日
        # code 和 startday必须按照按code排序、按start_day asc排序
        ind_codechange = np.diff(code) # 找到数据中股票切换的位置
        index_change = ind_codechange != 0 # 转化成bool值股票切换位置
        ind_codechange = np.append(index_change, np.array([True])) # 补上最后一位的True

        end_date = np.append(start_date[1:], np.array([last_end_date])) # 每一条记录的enddate都是下一条记录的startdate
        end_date[ind_codechange] = last_end_date # 对于切换位置的，则enddate用last_endday填充
        return end_date

    def data2mat(self, innercode_list, tradingdate, innercode, startdate, enddate, datadate, data):
        # pdb.set_trace()
        ndata = len(innercode)
        ndate = len(tradingdate)
        nstock = len(innercode_list)
        ind_notdrop = np.array([True] * ndata)
        innercode_list = innercode_list.astype(int)
        code_list = innercode.unique()
        for code in code_list:
            indcode = innercode == code
            cummaxdate = pd.Series.cummax(datadate[indcode])
            ind_notdrop[indcode] = datadate[indcode] >= cummaxdate

        innercode_array = innercode.values[ind_notdrop]
        startdate_array = startdate.values[ind_notdrop]
        enddate_array = enddate.values[ind_notdrop]
        data_array = data.values[ind_notdrop]

        tradingdate_list = tradingdate.values
        ndata = len(innercode_array)
        result_tab = np.ones([ndate, nstock]) * np.nan
        # tradingdate = pd.Series(list(map(pd.Timestamp, tradingdate) ))
        # pdb.set_trace()
        for index in range(ndata):
            # print ("row[startdate] = ", row['startdate'] , " type is ", type(row['startdate']))
            # print ("tradingdate = ", tradingdate, ", tpe is", type(tradingdate[0]))
            ind_date = \
            np.nonzero((tradingdate_list >= startdate_array[index]) & (tradingdate_list <= enddate_array[index]))[0]
            ind_stock = np.nonzero(innercode_list == innercode_array[index])[0]
            # pdb.set_trace()
            if (len(ind_date) > 0) & (len(ind_stock) > 0):
                result_tab[ind_date, ind_stock] = data_array[index]

        result_tab = pd.DataFrame(index=tradingdate_list, columns=innercode_list, data=result_tab)
        # pdb.set_trace()
        return result_tab