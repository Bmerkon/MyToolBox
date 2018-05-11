function foutname=txtstrreplace(finname,linetofind,replacedline)
%% 用于复制finname作为文件名对应的文件，同时将部分finname中的文字替换成新的文字
% finname：被替换的文件文件名
% linetofind：n*1的cell，每个cell包含一个需要被替换的str
% replacedline：n*1的cell，每个cell包含的str为对应linetofind的替换str

% 打开文件
fin=fopen(finname);
% 建立空文件为'tempsql.sql'
foutname='tempsql.sql';
fout=fopen(foutname,'w');
% 如果进来的linetofind不是cell格式的，说明只有一个词需要替换，那么先包装成cell
if ischar(linetofind)
    linetofind={linetofind};
    replacedline={replacedline};
end

n=size(linetofind,1);
while ~feof(fin)
    s=fgetl(fin); % 读取一行
    for i=1:n
        if ~isempty(strfind(s,linetofind(i))) % 如果该行满足被替换的条件
            s=replacedline{i};
            break
        end
    end
    fprintf(fout,'%s\n',s); % 输入到fout中
end
% 关闭文件
fclose(fin);
fclose(fout);
end