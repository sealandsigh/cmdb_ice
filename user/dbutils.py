# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/6/24

import traceback
from django.db import connection


class DBconnection(object):

    @classmethod
    def execute_mysql(cls,sql,args=(),fetch=True,one=False,curs=True):
        cnt,result = 0,None
        conn,cur = None,None
        try:
            if curs:
                cur = connection.cursor()
            else:
                cur = connection.cursor()
            cnt = cur.execute(sql,args)
            if fetch:
                result = cur.fetchone() if one else cur.fetchall()
            else:
                connection.commit()
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
        finally:
            if cur:
                cur.close()
        return cnt,result

