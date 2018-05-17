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
),

dvid as
(
select s.InnerCode,
s.RightRegDate as ��Ȩ�Ǽ���1,
s.BonusShareRatio as �͹�,
s.TranAddShareRaio as ת��,
s.CashDiviRMB as ÿ�ɷֺ�
from LC_Dividend as s
where  s.InnerCode in (select InnerCode from seclist)
and s.RightRegDate is not null
and s.EventProcedure=3131
and s.ifdividend=1
and s.RightRegDate between ? and ?
--order by s.innercode
),

place as
(
select s.innercode,s.RightRegDate as ��Ȩ�Ǽ���2,s.actualplaratio,s.plaprice from LC_ASharePlacement as s
where  s.InnerCode in (select InnerCode from seclist)
and s.RightRegDate is not null
and s.PlaPrice is not null
and s.RightRegDate between ? and ?
--order by s.innercode
),

reform as
(
select seclist.innercode,
s.ImplementionRecordDate as ��Ȩ�Ǽ���3,
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
and s.ImplementionRecordDate between ? and ?
--order by seclist.innercode,s.RecoverTradinDate;
)

select dvid.innercode as innercode1,place.innercode as innercode2,reform.innercode as innercode3,
dvid.��Ȩ�Ǽ���1,place.��Ȩ�Ǽ���2,reform.��Ȩ�Ǽ���3,
dvid.�͹�,dvid.ת��,dvid.ÿ�ɷֺ�,
place.actualplaratio ʮ��n,place.plaprice as ��ɼ�,
reform.��˾�͹�,reform.��˾ת����,reform.��˾����,reform.�Լ۹ɷ�,reform.�Լ��ֽ�
from
(reform full outer join dvid on dvid.innercode=reform.innercode and dvid.��Ȩ�Ǽ���1=reform.��Ȩ�Ǽ���3)
full outer join place on
(
(reform.innercode=place.innercode and reform.��Ȩ�Ǽ���3=place.��Ȩ�Ǽ���2)
or
(dvid.innercode=place.innercode and dvid.��Ȩ�Ǽ���1=place.��Ȩ�Ǽ���2)
)
order by
dvid.innercode,dvid.��Ȩ�Ǽ���1

