function datamat=data2mat_one(scodeList,tradingDayList,scode,dates,data)
% 调用这个函数的要求为：scode, startdate,data三元一体，为数据的本来三列，
% 并且order by scode then startdate，且每日数据不同，不需要前值填充空白

%% 初始化
ndate=size(tradingDayList,1);
nstock=size(scodeList,1);
datamat=nan(ndate,nstock);
for i=1:nstock
    % 找到开头
    indstart=find(scode==scodeList(i),1,'first');
    % 找到结尾
    indend=find(scode==scodeList(i),1,'last');
    idates=dates(indstart:indend);
    idata=data(indstart:indend);
    [~,a,b]=intersect(idates,tradingDayList);
    datamat(b,i)=idata(a,1);
end

end