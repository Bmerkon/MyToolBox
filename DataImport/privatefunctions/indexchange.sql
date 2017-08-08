select IndexInnerCode,SecuInnerCode,InDate,OutDate,Flag
from LC_IndexComponent
where IndexInnerCode in ('3145','46','4978')
order by IndexInnerCode,InDate asc

