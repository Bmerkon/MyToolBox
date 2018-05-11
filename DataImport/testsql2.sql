select datetime, ticker, open,high,low,close,volume,openinterest from futbars
where
datetime>='2017-03-01'
and
datetime<='2090-07-01'
and
ticker like 'SR%'
order by
ticker,datetime