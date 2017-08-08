function datamat=data2mat(scodeList,tradingDayList,scode,startdate,enddate,datadate,data)
%% 调用这个函数的要求为：scode, startdate,data三元一体，为数据的本来三列，并且order by scode then startdate
%% datadate表示数据对应的日期，比如我3日报告2日日期，datadate就是2，startdate就是3。如果新报告日报告的却是老对应日期，则不更新

%% 如果没有enddate，数据默认填充至下一个startdate出现
if isempty(enddate)
    enddate=[startdate(2:end)-1;tradingDayList(end)]; %i行的enddate就是i+1行startdate的前一日，最后一个数据填充为最后一日
    enddate([diff(scode)~=0;true])=tradingDayList(end); %切换股票的地方，enddate设置为最后一日
end
%% 初始化
ndate=size(tradingDayList,1);
nstock=size(scodeList,1);
datamat=nan(ndate,nstock);
tempstock=nan;
tempdatadate=-1;
%% 填充
for i=1:size(scode,1)
    indstock=find(scodeList==scode(i),1,'first');
    if indstock~=tempstock % 另一个股票
        tempstock=indstock; % 初始化当前股票
        tempdatadate=-1; % 初始化当前datadate
        tempdata=nan; %初始化当前数据值
    end
    istart=find(tradingDayList>=startdate(i),1,'first');
    iend=find(tradingDayList<=enddate(i),1,'last');
    if datadate(i)>=tempdatadate % 如果数据对应日期更新了，数据才更新
        datamat(istart:iend,indstock)=data(i);
        tempdatadate=datadate(i);
        tempdata=data(i);
    else % 否则即使报告日期更新了，数据还是使用老数据
        datamat(istart:iend,indstock)=tempdata;
    end
    
    
end
end


