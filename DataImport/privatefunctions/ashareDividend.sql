with
seclist as
(
select distinct
	s.SecuCode ,s.companycode, s.InnerCode,s.ChiName,s.ListedDate,z.MS as '½»Ò×Ëù',u.MS as '×´Ì¬',s.SecuAbbr
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
--select s.*  from LC_Dividend as s
select s.InnerCode,s.ExDiviDate,s.CashDiviRMB
from LC_Dividend as s
where  s.InnerCode in (select InnerCode from seclist)
and s.ExDiviDate is not null
and s.EventProcedure=3131
and s.ifdividend=1
and s.ExDiviDate between '2005-01-01' and '2016-01-01'
order by s.innercode


