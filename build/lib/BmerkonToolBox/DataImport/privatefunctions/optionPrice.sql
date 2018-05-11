select q.InnerCode,q.TradingDate,q.ClosePrice
from 
	Opt_DailyQuote as q
where
    q.TradingDate between '2005-01-01' and '2016-01-01'
and 
    q.OpenPrice<>0
order by InnerCode asc, TradingDate asc

