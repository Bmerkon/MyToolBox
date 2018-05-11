function datamat=data2mat(scodeList,tradingDayList,scode,startdate,enddate,datadate,data)
%% �������������Ҫ��Ϊ��scode, startdate,data��Ԫһ�壬Ϊ���ݵı������У�����order by scode then startdate
%% datadate��ʾ���ݶ�Ӧ�����ڣ�������3�ձ���2�����ڣ�datadate����2��startdate����3������±����ձ����ȴ���϶�Ӧ���ڣ��򲻸���

%% ���û��enddate������Ĭ���������һ��startdate����
if isempty(enddate)
    enddate=[startdate(2:end)-1;tradingDayList(end)]; %i�е�enddate����i+1��startdate��ǰһ�գ����һ���������Ϊ���һ��
    enddate([diff(scode)~=0;true])=tradingDayList(end); %�л���Ʊ�ĵط���enddate����Ϊ���һ��
end
%% ��ʼ��
ndate=size(tradingDayList,1);
nstock=size(scodeList,1);
datamat=nan(ndate,nstock);
tempstock=nan;
tempdatadate=-1;
%% ���
for i=1:size(scode,1)
    indstock=find(scodeList==scode(i),1,'first');
    if indstock~=tempstock % ��һ����Ʊ
        tempstock=indstock; % ��ʼ����ǰ��Ʊ
        tempdatadate=-1; % ��ʼ����ǰdatadate
        tempdata=nan; %��ʼ����ǰ����ֵ
    end
    istart=find(tradingDayList>=startdate(i),1,'first');
    iend=find(tradingDayList<=enddate(i),1,'last');
    if datadate(i)>=tempdatadate % ������ݶ�Ӧ���ڸ����ˣ����ݲŸ���
        datamat(istart:iend,indstock)=data(i);
        tempdatadate=datadate(i);
        tempdata=data(i);
    else % ����ʹ�������ڸ����ˣ����ݻ���ʹ��������
        datamat(istart:iend,indstock)=tempdata;
    end
    
    
end
end


