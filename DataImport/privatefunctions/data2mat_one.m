function datamat=data2mat_one(scodeList,tradingDayList,scode,dates,data)
% �������������Ҫ��Ϊ��scode, startdate,data��Ԫһ�壬Ϊ���ݵı������У�
% ����order by scode then startdate����ÿ�����ݲ�ͬ������Ҫǰֵ���հ�

%% ��ʼ��
ndate=size(tradingDayList,1);
nstock=size(scodeList,1);
datamat=nan(ndate,nstock);
for i=1:nstock
    % �ҵ���ͷ
    indstart=find(scode==scodeList(i),1,'first');
    % �ҵ���β
    indend=find(scode==scodeList(i),1,'last');
    idates=dates(indstart:indend);
    idata=data(indstart:indend);
    [~,a,b]=intersect(idates,tradingDayList);
    datamat(b,i)=idata(a,1);
end

end