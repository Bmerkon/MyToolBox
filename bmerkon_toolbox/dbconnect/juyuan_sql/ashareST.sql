 --select * from CT_SystemConst
 --where LB=1185



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


select innercode,specialtradetype,specialtradetime from LC_SpecialTrade
where 
innercode in (select InnerCode from seclist)
order by innercode asc,specialtradetime asc