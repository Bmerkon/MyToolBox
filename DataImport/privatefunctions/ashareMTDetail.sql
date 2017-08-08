select InnerCode,TradingDay,SecurityVolume 
from MT_TradingDetail
where 
TradingDay between '2010-01-01' and '2016-12-31'
and
SecurityVolume is not null
order by
InnerCode,TradingDay