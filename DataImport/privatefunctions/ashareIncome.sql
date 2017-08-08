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

select distinct seclist.innercode, s.UpdateTime,s.enddate, s.eps
from 
LC_IncomeStatementAll as s left join seclist on s.companycode=seclist.companycode
where s.companycode in (select companycode from seclist)
and s.IfAdjusted=2
and s.IfMerged=1
and s.AccountingStandards=1
and s.bulletinType=20
and month(s.enddate)=12
order by seclist.innercode asc,s.InfoPublDate asc 