
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


select q.InnerCode,q.TradingDay,q.TurnoverVolume
from 
	QT_DailyQuote as q
where
	q.InnerCode in (select InnerCode from seclist)
and
    q.TradingDay between '2005-01-01' and '2016-01-01'
order by InnerCode asc, TradingDay asc
