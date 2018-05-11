select InnerCode,EndDate,Weight
from LC_IndexComponentsWeight
where IndexCode = 3145
and
EndDate between '2005-01-01' and '2016-01-01'
order by InnerCode asc,EndDate asc