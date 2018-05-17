with
seclist as
(
select distinct
	s.SecuCode ,s.companycode, s.InnerCode,s.ChiName,s.ListedDate,z.MS as '交易所',u.MS as '状态',s.SecuAbbr
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


select seclist.innercode,
s.companycode,
s.recovertradindate,
ss.CompanyGrantedShare as 公司送股,
ss.CompanyTransformedShare as 公司转增股,
ss.CompanyPaidCashBT as 公司派现,
ss.ShareConsiderationRate as 对价股份,
ss.CashConsiderationRateBT as 对价现金
from (LC_ShareMergerReform as s left join LC_RConsideration as ss on s.companycode = ss.companycode)
left join seclist on s.companycode = seclist.companycode
where 
s.companycode in (select companycode from seclist)
and s.process=3131
and ss.ifeffected=1
and s.recovertradindate between '2005-01-01' and '2016-01-01'
order by seclist.innercode,s.RecoverTradinDate;




