select datetime,ticker,open,high,low,close,turnover,volume from stkbars
where
datetime>=%(t1)s
and 
datetime<=%(t2)s
order by
ticker,datetime