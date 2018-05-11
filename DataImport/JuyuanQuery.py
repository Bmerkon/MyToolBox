import pyodbc as db_odbc
import psycopg2 as db_pgs
import pandas as pd
import numpy as np
import datetime
import pdb



class JuYuanDB:
    def __init__(self):
        self.conn = db_odbc.connect('DSN=JuYuan;UID=JYUSER;PWD=jyuser123456')
        self.sql_fpath = 'D:\OneDrive\pythonwork\MyToolBox\DataImport\privatefunctions'
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
        sql_data['info_publdate']=sql_data['data_date'].copy()
        #print('success')
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
    def query_stockquote(self,stock_innercode,name,first_day,last_day,mode='mat'):
        sql = self.file2query('asharePrice.sql')
        sql = sql.replace('MySelected', name)
        sql_data = pd.read_sql(sql, self.conn, params=[first_day, last_day])

        sql_data['info_publdate']=sql_data['TradingDay']
        sql_data.columns = ['innercode', 'info_publdate', name,'data_date']
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, name, ffill=False,mode=mode)
        return data_mat

    # 移植上市日期
    def query_listed2now(self, stock_innercode,first_day,last_day):
        stockinfo=self.query_stockinfo()
        tradingdate=self.query_tradingday(first_day, last_day)

        def date2now(column,stockinfo,tradingdate):
            code=column.name
            #pdb.set_trace()
            if code in stockinfo.index:
                return tradingdate['TradingDate']-stockinfo.loc[code,'ListedDate']

        listed2now=pd.DataFrame(index=tradingdate['TradingDate'],columns=stock_innercode)
        listed2now=listed2now.apply(axis=0,func=date2now,args=(stockinfo,tradingdate))
        listed2now.index=tradingdate['TradingDate']
        return listed2now


    # 移植ST
    def query_ST(self, stock_innercode,first_day,last_day,mode='mat'):
        sql=self.file2query('ashareST.sql')
        sql_data = pd.read_sql(sql, self.conn)

        def resettype(sttype):
            # 该函数把聚源中的ST类型转化成我们需要的ST类型
            sttype2=sttype.copy()
            sttype2[(sttype==2) | (sttype==4)|(sttype==6)]=0
            sttype2[(sttype==1) |(sttype==7)]=1
            sttype2[(sttype==5) |(sttype==8)]=2
            sttype2[(sttype==3)]=3
            sttype2[(sttype==9)]=4
            sttype2[(sttype==10)]=5
            return sttype2
        
        # ST类型转化
        sttype_new=resettype(sql_data['specialtradetype'])
        sql_data['specialtradetype']=sttype_new.values

        sql_data['data_date']=sql_data['specialtradetime']
        sql_data.columns=['innercode','STtype', 'info_publdate', 'data_date']
        #pdb.set_trace()
        data_mat = self.process_data(stock_innercode, first_day, last_day, sql_data, 'STtype', ffill=True,mode=mode)
        if mode=='mat':
            data_mat.fillna(0,inplace=True)

        # 额外输出一下ST类型与数字
        ST_list=pd.DataFrame({'ST_num':range(6),
                      'ST_type':[
                          '正常',
                          'ST',
                          '*ST',
                          'PT',
                          '退市整理器',
                          '高风险提示'
                      ]
        })

        return data_mat,ST_list

    # 读取单个index或者股票数据
    def query_singlequote(self, code,name,first_day,last_day,type='stock'):
        if type=='stock':
            tbname='QT_DailyQuote'
            secuCat=1
        elif type=='index':
            tbname='QT_IndexQuote'
            secuCat=4
        #code_new='\''+code+'\''
        #pdb.set_trace() 
        #print(1)
        
        sql = self.file2query('ashareQuoteIndex_single.sql')
        sql=sql.replace('name',name,1)
        sql=sql.replace('tbname',tbname)
        #pdb.set_trace()
        sql_data = pd.read_sql(sql, self.conn, params=[secuCat,code,first_day, last_day])
        sql_data.set_index('Tradingday',inplace=True)
        return sql_data

    # 读取index成分股股票数据
    def query_indexcomp(self, stock_innercode,index_innercode,first_day,last_day,mode='mat'):
        sql = self.file2query('indexchange.sql')
        sql_data = pd.read_sql(sql, self.conn,params=[index_innercode])

        indin=sql_data[['SecuInnerCode','InDate']].copy()
        indin.columns=['innercode','info_publdate']
        indin['flag']=1
        
        indout=sql_data[['SecuInnerCode','OutDate']][sql_data['Flag']==0].copy()
        indout.columns=['innercode','info_publdate']
        indout['flag']=0

        indinout=pd.concat([indin,indout]).reset_index(drop =True)
        #pdb.set_trace()
        indinout['data_date']=indinout['info_publdate']

        
        indinout.columns = ['innercode', 'info_publdate', 'flag','data_date']
        #print('success')
        data_mat = self.process_data(stock_innercode, first_day, last_day, indinout, 'flag', ffill=True,mode=mode)
        return data_mat


    # Restore Factor移植
    def query_restoref(self,stock_innercode,first_day,last_day,mode='mat',close=None):
        sql = self.file2query('ashareRestore.sql')
        sql_data = pd.read_sql(sql, self.conn, params=[first_day, last_day,first_day, last_day,first_day, last_day])
        #pdb.set_trace()
        # 把几列合并成1列，如：[nan,1,nan]合并成1
        sql_data['innercode']=sql_data['innercode1'].fillna(sql_data['innercode2']).fillna(sql_data['innercode3'])
        sql_data['股权登记日1'] = (sql_data['股权登记日1'].fillna(pd.NaT)) # 确保最后输出能是日期，否则就会变成int，导致问题
        sql_data['info_publdate']=sql_data['股权登记日1'].fillna(sql_data['股权登记日2']).fillna(sql_data['股权登记日3'])
        sql_data.drop(labels=['innercode1','innercode2','innercode3','股权登记日1','股权登记日2','股权登记日3'],axis=1,inplace=True)

        # 需要收盘价（登记日的收盘价，就是股价复权使用的前收盘价）
        if close is None:
            close=self.query_stockquote(stock_innercode,'ClosePrice',first_day,last_day,mode='tab')

        # 合并两者（计入股权登记日收盘价）
        sql_new=pd.merge(sql_data, close, how='left', on=['innercode','info_publdate'])

        # 处理没有前收盘的数据
        def find_preclose(row):
            inda=(close['innercode']==row['innercode'])&(close['data_date']<row['info_publdate'])
            p=close['ClosePrice'][inda].values
            if len(p)>0:
                return p[-1]
            else:
                return None
        #pdb.set_trace()
        
        pre_close_lack=sql_new[sql_new['ClosePrice'].isnull()]
        if not pre_close_lack.empty:# 如果所有数据都有preclose，那也就不用调整
            pre_close_lack['ClosePrice']=pre_close_lack.apply(find_preclose,axis=1)
            sql_new.update(pre_close_lack[['innercode','ClosePrice']])
        #pdb.set_trace()
        sql_new.dropna(subset=['ClosePrice'],inplace=True)
        sql_new.fillna(0,inplace=True)

        L=(sql_new['送股']+sql_new['转增']+sql_new['公司送股']+sql_new['公司转增股']+sql_new['对价股份'])/10
        M=sql_new['十配n']/10
        D=(sql_new['每股分红']+sql_new['公司派现']+sql_new['对价现金'])/10
        Q=sql_new['配股价']
        sql_new['restore_factor']=(sql_new['ClosePrice']+Q*M-D)/(sql_new['ClosePrice']*(1+L+M))
        sql_data=sql_new[['innercode','info_publdate', 'data_date','restore_factor']]
        sql_data['data_date']=sql_data['info_publdate'].values # 确保datadate不会有奇异值都能生效

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
        data_mat=df.pivot_table(index='info_publdate',columns='innercode',values=value_name,aggfunc='last')
        #pdb.set_trace()
        # 增加必要的第一行，确保改行能被填充前值的有效数据
        #if tradingdate_list[0] not in data_mat.index:
        #    data_mat.loc[tradingdate_list[0]]=np.nan
        #    data_mat.sort_index(inplace=True)
        #if ffill:
        #    data_mat.fillna(method='ffill',inplace=True)

        # 处理成要求的mat
        # 整合数据日期和我们要求的日期
        union_date=tradingdate['TradingDate'].append(data_mat.index.to_series()).reset_index(drop=True).sort_values().unique()
        final_mat=pd.DataFrame(index=union_date,columns=innercode_list)
        final_mat.update(data_mat)
        if ffill:
            final_mat.fillna(method='ffill',inplace=True)
        final_mat=final_mat.loc[tradingdate_list,:]
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


    def datacombo(self,stock_innercode,first_day,last_day):
        # 读取收盘价信息
        close=self.query_stockquote(stock_innercode, 'closeprice', first_day, last_day, mode='mat')

        # 读取复权信息
        restoref=self.query_restoref(stock_innercode, first_day, last_day, mode='mat')
        restore_reverse=restoref.iloc[::-1]
        restore_reverse_cum=restore_reverse.cumprod()
        restore_f_cum=restore_reverse_cum.iloc[::-1]

        # 读取ST
        ST,ST_list=self.query_ST(stock_innercode,first_day,last_day,mode='mat')

        # 读取行业情况
        industry,industry_list=self.query_industry(stock_innercode, 'FirstIndustryName', first_day, last_day,mode='mat')

        # 读取上市天数
        listed2now=self.query_listed2now(stock_innercode,first_day,last_day)

        # 计算ret
        close_r=close*restore_f_cum
        ret=close_r.pct_change(1)

        # 设置字典
        data={}
        data['ret_qualified']=(ret<0.09)&(ret>-0.09)
        data['notST_qualified']=(ST==0)
        data['listed2now_qualified']= listed2now>180
        data['close']=close
        data['restore_f_cum']=restore_f_cum
        data['restore_f']=restoref
        data['industry']=industry
        data['ST']=ST
        data['listed2now']=listed2now
        data['close_r']=close_r
        data['ret']=ret

        # 整合成Panel
        #data=pd.Panel(data) (一整合就卡死)
        return data, industry_list,ST_list

    # 最后一步
    def process_data(self,innercode_list,first_day,last_day,df,value_name,ffill=False,mode='mat'):
        if mode == 'mat':
            data_mat = self.data2matnew(innercode_list,first_day,last_day,df,value_name,ffill=ffill)
            return data_mat
        else:
            return df

