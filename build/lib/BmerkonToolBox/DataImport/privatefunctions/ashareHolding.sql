with seclist
as
(
select distinct
	s.SecuCode ,s.companycode,s.innercode
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

select distinct seclist.innercode, s.UpdateTime as InfoPublDate,s.enddate, s.MySelected
from 
LC_StockHoldingSt as s left join seclist on s.companycode=seclist.companycode
where s.companycode in (select companycode from seclist)
and
s.MySelected is not null
order by seclist.innercode asc,s.UpdateTime asc,s.enddate 