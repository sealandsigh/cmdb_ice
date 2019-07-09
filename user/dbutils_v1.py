# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/6/24

# import MySQLdb
import traceback
# from MySQLdb import cursors
from django.db import connection

# MYSQL_HOST = '127.0.0.1'
# MYSQL_PORT = 3306
# MYSQL_USER = 'root'
# MYSQL_PASSWD = 'zhujiajun'
# MYSQL_DB = 'zhujiajun'
# MYSQL_CHARSET = 'utf8'

class DBconnection(object):

    @classmethod
    def execute_mysql(cls,sql,args=(),fetch=True,one=False,curs=True,commlimit=False,execline=1,limitline=1,closelimit=True):
        cnt,result = 0,None
        conn,cur = None,None
        try:
            # conn = connection(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,
            #                        passwd=MYSQL_PASSWD,db=MYSQL_DB,charset=MYSQL_CHARSET)
            if curs:
                cur = connection.cursor()
                # cur = connection.cursor(cursors.DictCursor)
            else:
                cur = connection.cursor()
            cnt = cur.execute(sql,args)
            if fetch:
                result = cur.fetchone() if one else cur.fetchall()
            else:
                if commlimit:
                    if execline % limitline == 0:
                        # conn.commit()
                        connection.commit()
                else:
                    # conn.commit()
                    connection.commit()
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
        finally:
            if closelimit:
                if cur:
                    cur.close()
                # if conn:
                #     conn.close()
        return cnt,result

