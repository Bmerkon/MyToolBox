select q.TradingDay,q.OpenPrice,q.highprice,q.lowprice,q.closeprice,q.TurnoverVolume,q.OpenInterest
from Fut_TradingQuote as q
where
    q.ContractCode='IF1501'
and
    q.TradingDay between '2010-01-01'and '2016-12-31'
order by q.TradingDay