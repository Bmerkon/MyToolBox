function [Anew,firstallnotnan]=replacenan(A,retainnan) %调节价格矩阵prices，价格如果为nan就用前值代替
% A为nperiods*p的数值矩阵，其中有些值为nan
if nargin==1
    retainnan=false;
end

nump=size(A,2);
numv=size(A,1);
% 确保倒推是一定可以开始的，额外加一行辅助行0
A=[zeros(1,nump);A];
% 找出所有的nan元素
indNaN=isnan(A);
% 找出每一列第一个没有nan元素的行的位置，以确保后面每一行都至少有一个前值（如果从头开始一直都有nan元素，那就不行）
firstnotnan=zeros(1,nump);
for i=1:nump
    f=find(~indNaN(2:end,i),1);
    if isempty(f)
        firstnotnan(i)=numv+2;
    else
        firstnotnan(i)=f+1;
    end
end
% 这是最终能开始使用A的行
firstallnotnan=max(firstnotnan);
% 看看哪些行是有nan的
indexistnan=find(sum(indNaN,2));
for i=1:size(indexistnan,1)%迭代每一行的NaN部分都由前一行的对应位置代替
    A(indexistnan(i),indNaN(indexistnan(i),:))=...,
        A(indexistnan(i)-1,indNaN(indexistnan(i),:));
end
% 获得最终的A
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