# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/6/25

'''
create table accesslog(
    id int primary key auto_increment,
    logtime datetime not null,
    ip varchar(256) not null default '',
    url varchar(1024) not null default '',
    status int not null default 0
) engine=innodb default charset utf8;
'''
import MySQLdb
from datetime import datetime

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'zhujiajun'
MYSQL_DB = 'zhujiajun1'
MYSQL_CHARSET = 'utf8'


SQL_INSERT_ACCESSLOG = 'INSERT INTO accesslog(logtime,ip,url,status) VALUES(%s,%s,%s,%s)'
params = {
    'host':MYSQL_HOST,
    'port':MYSQL_PORT,
    'user':MYSQL_USER,
    'passwd':MYSQL_PASSWD,
    'db':MYSQL_DB,
    'charset':MYSQL_CHARSET
}

if __name__ == '__main__':
    with open('access.1w.log','rt') as fhandler:
        conn = MySQLdb.connect(**params)
        cur = conn.cursor()
        cnt = 0
        for line in fhandler:
            line = line.split()
            ip = line[0]
            url = line[6]
            status = line[8]
            logtime = line[3]
            logtime = logtime[1:]
            logtime = datetime.strptime(logtime, '%d/%b/%Y:%H:%M:%S')
            logtime = logtime.strftime('%Y-%m-%d %H:%M:%S')
            args = (logtime,ip,url,status)
            cnt += cur.execute(SQL_INSERT_ACCESSLOG,args)
            if cnt % 100 == 0:
                conn.commit()
        conn.commit()
        cur.close()
        conn.close()