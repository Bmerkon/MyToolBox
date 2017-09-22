select date, ticker, open,high,low,close,settle,volume,openinterest from futdaily
where
date>='2017-02-20'
and
date<='2090-07-30'
order by
date, ticker