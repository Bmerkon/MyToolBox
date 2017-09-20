import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import datetime
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

    # balancesheet移植
    def query_balance(self, stock_innercode, name, firstday, lastday, indenddate='All'):

        sql = self.file2query('ashareBalance.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)
        # print(stock_innercode)
        # print(tradingdate)
        # print(sql_data['innercode'])
        # print(sql_data['InfoPublDate'])
        # print(sql_data['info_enddate'])
        # print(sql_data['enddate'])
        # print(sql_data[name])
        # pdb.set_trace()
        # return sql_data
        return data_mat

    # cashflow移植
    def query_cashflow(self,stock_innercode, name, firstday, lastday, indenddate='All'):
        sql = self.file2query('ashareCashFlow.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)

        return data_mat

    # dividend移植
    def query_dividend(self,stock_innercode, name, firstday, lastday):
        sql = self.file2query('ashareDividend.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn, params=[firstday,lastday])
        tradingdate = self.query_tradingday(firstday, lastday)
        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['ExDiviDate'].values, sql_data['ExDiviDate'].values,
                                 sql_data['ExDiviDate'].values, sql_data[name].values)

        return data_mat

    # 股东数量移植
    def query_holder(self,stock_innercode, name, firstday, lastday):
        sql = self.file2query('ashareHolderInfo.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        inda = sql_data['InfoPublDate'].isnull()
        oneM=datetime.timedelta(days=30)
        sql_data['InfoPublDate'][inda] = sql_data['enddate'][inda] + oneM

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)
        return data_mat

    # 股东结构移植
    def query_holding(self,stock_innercode, name, firstday, lastday):
        sql = self.file2query('ashareHolding.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)
        return data_mat

    # income移植
    def query_income(self,stock_innercode, name, firstday, lastday, indenddate='All'):
        sql = self.file2query('ashareIncome.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)

        return data_mat

    # capital移植
    def query_capital(self,stock_innercode, name, firstday, lastday):
        sql = self.file2query('ashareCapital.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        tradingdate = self.query_tradingday(firstday, lastday)
        sql_data['info_enddate'] = self.find_end(sql_data['innercode'], sql_data['InfoPublDate'], tradingdate.iloc[-1])

        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['info_enddate'].values,
                                 sql_data['enddate'].values, sql_data[name].values)
        return data_mat

    # 移植industry
    def query_industry(self,stock_innercode, name, firstday, lastday):
        sql = self.file2query('ashareIndustry2.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        tradingdate = self.query_tradingday(firstday, lastday)

        ind_noenddate=sql_data['enddate'].isnull()
        sql_data.loc[ind_noenddate,'enddate']=tradingdate.iloc[-1].values # 我太强了，改值一定要用values

        industrySet=sql_data[name].unique()
        industry_num= np.ones([sql_data.shape[0],1]) * np.nan
        for i in range(industrySet.shape[0]):
            ind_industry=sql_data[name]==industrySet[i]
            industry_num[ind_industry]=i

        industry_list=pd.DataFrame(data=industrySet,columns=[name])
        industry_list['industry_num']=range(industrySet.shape[0])



        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['innercode'].values,
                                 sql_data['InfoPublDate'].values, sql_data['enddate'].values,
                                 sql_data['enddate'].values, industry_num)
        return data_mat,industry_list

    # 移植price
    def query_quote(self,stock_innercode,name,firstday,lastday):
        sql = self.file2query('asharePrice.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn, params=[firstday, lastday])
        tradingdate = self.query_tradingday(firstday, lastday)
        data_mat = self.data2mat(stock_innercode, tradingdate['TradingDate'].values, sql_data['InnerCode'].values,
                                 sql_data['TradingDay'].values, sql_data['TradingDay'].values,
                                 sql_data['TradingDay'].values, sql_data[name].values)

        return data_mat
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

    def data2mat(self, innercode_list, tradingdate_list, innercode, startdate, enddate, datadate, data):
        # pdb.set_trace()
        ndata = len(innercode)
        ndate = len(tradingdate_list)
        nstock = len(innercode_list)
        ind_notdrop = np.array([True] * ndata)
        innercode_list = innercode_list.astype(int)

        code_list = np.unique(innercode)
        datadate_serie=pd.Series(data=datadate)
        for code in code_list:
            indcode = innercode == code
            cummaxdate = pd.Series.cummax(datadate_serie[indcode])
            ind_notdrop[indcode] = datadate[indcode] >= cummaxdate

        innercode_array = innercode[ind_notdrop]
        startdate_array = startdate[ind_notdrop]
        enddate_array = enddate[ind_notdrop]
        data_array = data[ind_notdrop]
        #tradingdate_list = tradingdate_list.values
        ndata = len(innercode_array)
        result_tab = np.ones([ndate, nstock]) * np.nan
        # tradingdate_list = pd.Series(list(map(pd.Timestamp, tradingdate_list) ))
        # pdb.set_trace()
        for index in range(ndata):
            # print ("row[startdate] = ", row['startdate'] , " type is ", type(row['startdate']))
            # print ("tradingdate_list = ", tradingdate_list, ", tpe is", type(tradingdate_list[0]))
            ind_date = \
            np.nonzero((tradingdate_list >= startdate_array[index]) & (tradingdate_list <= enddate_array[index]))[0]
            ind_stock = np.nonzero(innercode_list == innercode_array[index])[0]
            # pdb.set_trace()
            if (len(ind_date) > 0) & (len(ind_stock) > 0):
                result_tab[ind_date, ind_stock] = data_array[index]

        result_tab = pd.DataFrame(index=tradingdate_list, columns=innercode_list, data=result_tab)
        # pdb.set_trace()
        return result_tab