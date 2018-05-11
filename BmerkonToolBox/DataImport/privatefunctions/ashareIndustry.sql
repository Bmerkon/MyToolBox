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


select distinct seclist.innercode, s.InfoPublDate,s.CancelDate,s.FirstIndustryName
from LC_ExgIndustry as s left join seclist on s.companycode=seclist.companycode
where s.companycode in (select companycode from seclist)
and
s.standard=9
order by seclist.innercode,s.InfoPublDate