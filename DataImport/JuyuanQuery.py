import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import datetime
import pdb



class JuYuanDB:
    def __init__(self):
        self.conn = db_odbc.connect('DSN=JuYuan;UID=JYUSER;PWD=jyuser123456')
        self.sql_fpath = 'D:\pythonwork\MyToolBox\DataImport\privatefunctions'
        self.firstday = '2010-01-01'
        self.lastday = '2017-06-01'
        #self.mode='mat'

    def file2query(self, filename):
        f = open((self.sql_fpath + '\\' + filename))
        sql = f.read()
        return sql

    # tradingday移植
    def query_tradingday(self, first_day, last_day):
        sql = self.file2query('tradingday.sql')
        tradingdate = pd.read_sql(sql, self.conn, params=[first_day, last_day])
        return tradingdate

    # stockinfo移植
    def query_stockinfo(self):
        sql = self.file2query('ashareList.sql')
        return pd.read_sql(sql, self.conn, index_col='InnerCode')

    # balancesheet移植
    def query_balance(self, stock_innercode, name, first_day, last_day, indenddate='All',mode='mat'):

        sql = self.file2query('ashareBalance.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])
        sql_data.columns=['innercode','info_publdate','data_date',name]

        data_mat= self.process_data(stock_innercode,first_day,last_day,sql_data,name,ffill=True,mode=mode)
        return data_mat

    # cashflow移植
    def query_cashflow(self,stock_innercode, name, first_day, last_day, indenddate='All',mode='mat'):
        sql = self.file2query('ashareCashFlow.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])
        sql_data.columns = ['innercode', 'info_publdate', 'data_date', name]

        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)
        return data_mat

    # dividend移植
    def query_dividend(self, stock_innercode, name, first_day, last_day,mode='mat'):
        sql = self.file2query('ashareDividend.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn, params=[first_day, last_day])
        sql_data['info_publdate']=sql_data['ExDiviDate']

        sql_data.columns = ['innercode', 'info_publdate', name, 'data_date']
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=False,mode=mode)
        return data_mat

    # 股东数量移植
    def query_holder(self,stock_innercode, name, first_day, last_day,mode='mat'):
        sql = self.file2query('ashareHolderInfo.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        inda = sql_data['InfoPublDate'].isnull()
        oneM=datetime.timedelta(days=30)
        sql_data['InfoPublDate'][inda] = sql_data['enddate'][inda] + oneM

        sql_data.columns = ['innercode', 'info_publdate', 'data_date',name]
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)
        return data_mat

    # 股东结构移植
    def query_holding(self,stock_innercode, name, first_day, last_day,mode='mat'):
        sql = self.file2query('ashareHolding.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        sql_data.columns = ['innercode', 'info_publdate', 'data_date', name]

        # 这里负责把时间简化到年月日，去掉小时等数据，否则后面对不齐
        sql_data['info_publdate']=sql_data['info_publdate'].values.astype('<M8[D]')
        idx=sql_data.groupby(by=['innercode','info_publdate'])['data_date'].idxmax()
        sql_data=sql_data.iloc[idx]

        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)
        return data_mat

    # income移植
    def query_income(self,stock_innercode, name, first_day, last_day, indenddate='All',mode='mat'):
        sql = self.file2query('ashareIncome.sql')
        sql = sql.replace('MySelected', name)
        if str(indenddate).capitalize() == 'All':
            sql = sql.replace('and month(s.enddate)=?', '')
            sql_data = pd.read_sql(sql, self.conn)
        else:
            sql_data = pd.read_sql(sql, self.conn, params=[indenddate])

        sql_data.columns = ['innercode', 'info_publdate', 'data_date', name]
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)
        return data_mat

    # capital移植
    def query_capital(self,stock_innercode, name, first_day, last_day,mode='mat'):
        sql = self.file2query('ashareCapital.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        sql_data.columns = ['innercode', 'info_publdate', 'data_date', name]
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)
        return data_mat

    # 移植industry
    def query_industry(self,stock_innercode, name, first_day, last_day,mode='mat'):
        sql = self.file2query('ashareIndustry2.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn)

        # 用数字代替行业文字
        industrySet=sql_data[name].unique()
        sql_data[name]=sql_data[name].replace(industrySet,range(industrySet.shape[0]))
        sql_data['data_date']=sql_data['InfoPublDate']

        sql_data.columns = ['innercode', 'info_publdate', name,'standard','data_date']
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=True,mode=mode)

        # 额外输出一下行业文字与数字
        industry_list=pd.DataFrame(data=industrySet,columns=[name])
        industry_list['industry_num']=range(industrySet.shape[0])

        return data_mat,industry_list

    # 移植price
    def query_quote(self,stock_innercode,name,first_day,last_day,mode='mat'):
        sql = self.file2query('asharePrice.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn, params=[first_day, last_day])

        sql_data['info_publdate']=sql_data['TradingDay']
        sql_data.columns = ['innercode', 'info_publdate', name,'data_date']
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=False,mode=mode)
        return data_mat

    # Restore Factor移植
    def query_restoref(self,stock_innercode,first_day,last_day,mode='mat'):
        sql = self.file2query('ashareRestore.sql')
        sql_data = pd.read_sql(sql, self.conn, params=[first_day, last_day,first_day, last_day,first_day, last_day])

        # 把几列合并成1列，如：[nan,1,nan]合并成1
        sql_data['innercode']=sql_data['innercode1'].fillna(sql_data['innercode2']).fillna(sql_data['innercode3'])
        sql_data['info_publdate']=sql_data['除息日'].fillna(sql_data['除权日']).fillna(sql_data['恢复交易日'])
        sql_data.drop(labels=['innercode1','innercode2','innercode3','除息日','除权日','恢复交易日'],axis=1,inplace=True)

        # 需要昨日收盘价
        pre_close=self.query_quote(stock_innercode,'PrevClosePrice',first_day,last_day,mode='tab')
        close=self.query_quote(stock_innercode,'ClosePrice',first_day,last_day,mode='tab')

        # 合并两者
        sql_new=pd.merge(sql_data, pre_close, how='left', on=['innercode','info_publdate'])

        # 处理没有前收盘的数据
        def find_preclose(row):
            inda=(close['innercode']==row['innercode'])&(close['data_date']<row['info_publdate'])
            p=close['ClosePrice'][inda].values
            if len(p)>0:
                return p[0]
            else:
                return None

        pre_close_lack=sql_new[sql_new['PrevClosePrice'].isnull()]
        pre_close_lack['PrevClosePrice']=pre_close_lack.apply(find_preclose,axis=1)
        sql_new.update(pre_close_lack[['innercode','PrevClosePrice']])
        #pdb.set_trace()
        sql_new.dropna(subset=['PrevClosePrice'],inplace=True)
        sql_new.fillna(0,inplace=True)

        L=(sql_new['送股']+sql_new['转增']+sql_new['公司送股']+sql_new['公司转增股']+sql_new['对价股份'])/10
        M=sql_new['十配n']/10
        D=(sql_new['每股分红']+sql_new['公司派现']+sql_new['对价现金'])/10
        Q=sql_new['配股价']
        sql_new['restore_factor']=(sql_new['PrevClosePrice']+Q*M-D)/(sql_new['PrevClosePrice']*(1+L+M))
        sql_data=sql_new[['innercode','info_publdate', 'data_date','restore_factor']]

        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, 'restore_factor', ffill=False, mode=mode)
        if mode=='mat':
            data_mat.fillna(1,inplace=True)
        return data_mat


    def data2matnew(self,innercode_list,first_day,last_day,df,value_name,ffill=False):
        # 计算日期
        tradingdate = self.query_tradingday(first_day, last_day)
        tradingdate_list=tradingdate['TradingDate'].values

        # 去除不合规的数据
        df.sort_values(by=['innercode','info_publdate','data_date'],inplace=True)
        gb=df.groupby('innercode')['data_date']
        df['latest_datadate']=gb.apply(lambda x:pd.Series.cummax(x))
        df=df[df['latest_datadate']<=df['data_date']] # 新数据日期总得早过最近数据，否则没有意义

        # 整理成新矩阵
        data_mat=df.pivot_table(index='info_publdate',columns='innercode',values=value_name)
        #pdb.set_trace()
        # 增加必要的第一行，确保改行能被填充前值的有效数据
        if tradingdate_list[0] not in data_mat.index:
            data_mat.loc[tradingdate_list[0]]=np.nan
            data_mat.sort_index(inplace=True)
        if ffill:
            data_mat.fillna(method='ffill',inplace=True)

        # 处理成要求的mat
        final_mat=pd.DataFrame(index=tradingdate_list,columns=innercode_list)
        final_mat.update(data_mat)
        if ffill:
            final_mat.fillna(method='ffill',inplace=True)
        return final_mat

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

    # 最后一步
    def process_data(self,innercode_list,first_day,last_day,df,value_name,ffill=False,mode='mat'):
        if mode == 'mat':
            data_mat = self.data2matnew(innercode_list,first_day,last_day,df,value_name,ffill=ffill)
            return data_mat
        else:
            return df