function foutname=txtstrreplace(finname,linetofind,replacedline)
%% ���ڸ���finname��Ϊ�ļ�����Ӧ���ļ���ͬʱ������finname�е������滻���µ�����
% finname�����滻���ļ��ļ���
% linetofind��n*1��cell��ÿ��cell����һ����Ҫ���滻��str
% replacedline��n*1��cell��ÿ��cell������strΪ��Ӧlinetofind���滻str

% ���ļ�
fin=fopen(finname);
% �������ļ�Ϊ'tempsql.sql'
foutname='tempsql.sql';
fout=fopen(foutname,'w');
% ���������linetofind����cell��ʽ�ģ�˵��ֻ��һ������Ҫ�滻����ô�Ȱ�װ��cell
if ischar(linetofind)
    linetofind={linetofind};
    replacedline={replacedline};
end

n=size(linetofind,1);
while ~feof(fin)
    s=fgetl(fin); % ��ȡһ��
    for i=1:n
        if ~isempty(strfind(s,linetofind(i))) % ����������㱻�滻������
            s=replacedline{i};
            break
        end
    end
    fprintf(fout,'%s\n',s); % ���뵽fout��
end
% �ر��ļ�
fclose(fin);
fclose(fout);
end