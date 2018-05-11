select SecuInnerCode,InDate,OutDate,Flag
from LC_IndexComponent
where IndexInnerCode=?
order by InDate asc


