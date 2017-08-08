function ttmdata=data2ttm(scode,yearlist,monthlist,data)
ttmdata=nan(size(data));
scodelist=unique(scode);
for i=1:size(scodelist,1) % ����ÿһֻ��Ʊ
   sstart=find(scode==scodelist(i),1,'first');%���ݿ�ʼ
   send=find(scode==scodelist(i),1,'last');%���ݽ���
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
    if monthlist(i)==3 %�����һ������ֱ�����
        ttmdata(i)=data(i);
    else % ����Ϊ2�����꣩��3��4���걨������
        indlasti=find(yearlist(1:i)==yearlist(i)&monthlist(1:i)==monthlist(i)-3 & datanotnan(1:i),1,'last');%�ҵ�ָ��ǰ���ȱ�������
        indi=~isempty(indlasti);
        if indi %����У��ǵ������ݼ�Ϊ���������ϼ�
            ttmdata(i)=data(i)-data(indlasti);
        else %���û�У��ǵ�������Ϊ��������/����
            ttmdata(i)=data(i)/(monthlist(i)/3);
        end
    end
end
end