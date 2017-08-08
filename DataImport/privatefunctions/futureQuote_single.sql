select q.enddate,q.OpenPrice,q.highprice,q.lowprice,q.closeprice,q.volume,q.openinterest 
from Fut_DailyQuote as q 
	left join Fut_ContractMain as p on q.InnerCode=p.ContractInnerCode
where
    p.ContractCode='RB1701'
and
    q.enddate between '2010-01-01' and '2016-12-31'
order by q.enddate