function ttmdata=data2ttm(scode,yearlist,monthlist,data)
ttmdata=nan(size(data));
scodelist=unique(scode);
for i=1:size(scodelist,1) % 对于每一只股票
   sstart=find(scode==scodelist(i),1,'first');%数据开始
   send=find(scode==scodelist(i),1,'last');%数据结束
   ttmdata(sstart:send,1)=data2ttmscodeq(yearlist(sstart:send,1),monthlist(sstart:send,1),data(sstart:send,1));
end
end

function ttmdata=data2ttmscode(yearlist,monthlist,data)
n=size(yearlist,1);
ttmdata=nan(size(data));
for i=1:n
    if monthlist(i)==12
        ttmdata(i)=data(i);
    else
        indlast12=find(yearlist(1:i)==yearlist(i)-1&monthlist(1:i)==12,1,'last');
        indlasti=find(yearlist(1:i)==yearlist(i)-1&monthlist(1:i)==monthlist(i),1,'last');
        ind12=~isempty(indlast12);
        indi=~isempty(indlasti);
        if ind12&&indi
            ttmdata(i)=data(i)+data(indlast12)-data(indlasti);
        elseif ind12&&~indi
            ttmdata(i)=data(indlast12);
        else
            ttmdata(i)=data(i)*12/monthlist(i);
        end
    end
end
end


function ttmdata=data2ttmscodeq(yearlist,monthlist,data)
n=size(yearlist,1);
ttmdata=nan(size(data));
datanotnan=~isnan(data);
for i=1:n
    if monthlist(i)==3 %如果是一季报，直接填充
        ttmdata(i)=data(i);
    else % 否则为2（半年）、3、4（年报）报表
        indlasti=find(yearlist(1:i)==yearlist(i)&monthlist(1:i)==monthlist(i)-3 & datanotnan(1:i),1,'last');%找到指定前季度报表数据
        indi=~isempty(indlasti);
        if indi %如果有，那单季数据即为当季减掉上季
            ttmdata(i)=data(i)-data(indlasti);
        else %如果没有，那单季数据为季度数据/季度
            ttmdata(i)=data(i)/(monthlist(i)/3);
        end
    end
end
end