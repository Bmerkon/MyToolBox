select distinct TradingDate from QT_TradingDayNew
where 
TradingDate between ? and ?
and 
IfTradingDay=1
and SecuMarket=83
order by TradingDate