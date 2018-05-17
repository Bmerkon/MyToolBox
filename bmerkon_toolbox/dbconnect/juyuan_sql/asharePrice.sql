
with seclist
as
(
select distinct
	s.SecuCode ,s.InnerCode
from 
	SecuMain as s,
	 CT_SystemConst as z,
	 CT_SystemConst as u
where SecuCategory=1 
	and SecuMarket in (90,83) 
	and ListedDate is not Null
	and s.SecuMarket=z.DM
	and z.LB=201
	and s.ListedState=u.DM
	and u.LB=1176
)


select q.InnerCode,q.TradingDay,q.MySelected
from 
	QT_DailyQuote as q
where
	q.InnerCode in (select InnerCode from seclist)
and
    q.TradingDay between ? and ?
and 
    q.OpenPrice<>0
order by InnerCode asc, TradingDay asc

