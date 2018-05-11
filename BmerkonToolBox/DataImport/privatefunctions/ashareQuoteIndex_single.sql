select Tradingday, name from tbname
where
Innercode in (
select s.innercode
from 
SecuMain as s
where SecuCategory=?
and 
SecuCode=?
)
and
TradingDay >=?
and
TradingDay<=?
order by Tradingday