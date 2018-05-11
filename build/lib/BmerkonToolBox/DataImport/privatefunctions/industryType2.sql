select distinct FirstIndustryName 
from LC_ExgIndustry
where 
Standard in (9,24)
order by FirstIndustryName