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
),

dvid as
(
select s.InnerCode,
s.ExDiviDate as 除息日,
s.BonusShareRatio as 送股,
s.TranAddShareRaio as 转增,
s.CashDiviRMB as 每股分红
from LC_Dividend as s
where  s.InnerCode in (select InnerCode from seclist)
and s.ExDiviDate is not null
and s.EventProcedure=3131
and s.ifdividend=1
and s.ExDiviDate between ? and ?
--order by s.innercode
),

place as
(
select s.innercode,s.exrightdate,s.actualplaratio,s.plaprice from LC_ASharePlacement as s
where  s.InnerCode in (select InnerCode from seclist)
and s.ExRightDate is not null
and s.PlaPrice is not null
and s.exrightdate between ? and ?
--order by s.innercode
),

reform as
(
select seclist.innercode,
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
and s.recovertradindate between ? and ?
--order by seclist.innercode,s.RecoverTradinDate;
)

select dvid.innercode as innercode1,place.innercode as innercode2,reform.innercode as innercode3,
dvid.除息日,place.exrightdate as 除权日,reform.recovertradindate as 恢复交易日,
dvid.送股,dvid.转增,dvid.每股分红,
place.actualplaratio 十配n,place.plaprice as 配股价,
reform.公司送股,reform.公司转增股,reform.公司派现,reform.对价股份,reform.对价现金
from  
(reform full outer join dvid on dvid.innercode=reform.innercode and dvid.除息日=reform.recovertradindate)
full outer join place on 
(
(reform.innercode=place.innercode and reform.recovertradindate=place.exrightdate) 
or
(dvid.innercode=place.innercode and dvid.除息日=place.exrightdate) 
)
order by
dvid.innercode,dvid.除息日


