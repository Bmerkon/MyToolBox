function conn=connectJYDB()
conn = database('JYDB','JYUSER','jyuser123456','com.microsoft.sqlserver.jdbc.SQLServerDriver','jdbc:sqlserver://192.168.1.21;database=JYDB');
% if ~isempty(conn.Message)
%     conn = database.ODBCConnection('JuYuan','JYUSER','jyuser123456');
% end
end