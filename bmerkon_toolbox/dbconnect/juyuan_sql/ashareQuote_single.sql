select q.TradingDay,q.OpenPrice,q.highprice,q.lowprice,q.closeprice,q.TurnoverVolume,q.TurnoverDeals
from QT_DailyQuote as q
where
    q.InnerCode=0000000
and
    q.TradingDay between '2010-01-01'and '2016-12-31'
order by q.TradingDay