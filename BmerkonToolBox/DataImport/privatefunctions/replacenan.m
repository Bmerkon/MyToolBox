function [Anew,firstallnotnan]=replacenan(A,retainnan) %���ڼ۸����prices���۸����Ϊnan����ǰֵ����
% AΪnperiods*p����ֵ����������ЩֵΪnan
if nargin==1
    retainnan=false;
end

nump=size(A,2);
numv=size(A,1);
% ȷ��������һ�����Կ�ʼ�ģ������һ�и�����0
A=[zeros(1,nump);A];
% �ҳ����е�nanԪ��
indNaN=isnan(A);
% �ҳ�ÿһ�е�һ��û��nanԪ�ص��е�λ�ã���ȷ������ÿһ�ж�������һ��ǰֵ�������ͷ��ʼһֱ����nanԪ�أ��ǾͲ��У�
firstnotnan=zeros(1,nump);
for i=1:nump
    f=find(~indNaN(2:end,i),1);
    if isempty(f)
        firstnotnan(i)=numv+2;
    else
        firstnotnan(i)=f+1;
    end
end
% ���������ܿ�ʼʹ��A����
firstallnotnan=max(firstnotnan);
% ������Щ������nan��
indexistnan=find(sum(indNaN,2));
for i=1:size(indexistnan,1)%����ÿһ�е�NaN���ֶ���ǰһ�еĶ�Ӧλ�ô���
    A(indexistnan(i),indNaN(indexistnan(i),:))=...,
        A(indexistnan(i)-1,indNaN(indexistnan(i),:));
end
% ������յ�A
if retainnan
    Anew=nan(size(A));
    for i=1:size(A,2)
        Anew(firstnotnan(i):end,i)=A(firstnotnan(i):end,i);
    end
    Anew=Anew(2:end,:);
else
    Anew=A(firstallnotnan:end,:);
end
end