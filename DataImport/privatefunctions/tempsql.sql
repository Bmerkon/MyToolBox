select q.InnerCode,q.TradingDate,q.ClosePrice
from 
	Opt_DailyQuote as q
where
q.TradingDate between '2015-02-09' and '2017-05-04'
and 
    q.OpenPrice<>0
order by InnerCode asc, TradingDate asc

