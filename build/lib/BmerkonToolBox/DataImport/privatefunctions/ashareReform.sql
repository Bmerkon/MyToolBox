with
seclist as
(
select distinct
	s.SecuCode ,s.companycode, s.InnerCode,s.ChiName,s.ListedDate,z.MS as '������',u.MS as '״̬',s.SecuAbbr
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
ss.CompanyGrantedShare as ��˾�͹�,
ss.CompanyTransformedShare as ��˾ת����,
ss.CompanyPaidCashBT as ��˾����,
ss.ShareConsiderationRate as �Լ۹ɷ�,
ss.CashConsiderationRateBT as �Լ��ֽ�
from (LC_ShareMergerReform as s left join LC_RConsideration as ss on s.companycode = ss.companycode)
left join seclist on s.companycode = seclist.companycode
where 
s.companycode in (select companycode from seclist)
and s.process=3131
and ss.ifeffected=1
and s.recovertradindate between '2005-01-01' and '2016-01-01'
order by seclist.innercode,s.RecoverTradinDate;




