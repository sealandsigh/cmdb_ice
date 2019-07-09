#encoding: utf-8

import json
import MySQLdb

from .dbutils import DBconnection
from django.db import models

# Create your models here.
class User(object):
    SQL_LOGIN = 'select id,name,age,sex,tel from user2 where name=%s and password=%s limit 1'
    SQL_GET_USERS = 'select id,name,age,sex,tel from user2'
    SQL_GET_USER = 'SELECT id,name,age,sex,tel FROM user2 WHERE id=%s'
    SQL_GET_USER_BY_NAME = 'SELECT id,name,age,sex,tel,password FROM user2 WHERE name=%s'
    SQL_UPDATE_USER = 'UPDATE user2 SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s'
    SQL_DELETE_USER = 'DELETE FROM user2 WHERE id=%s'
    SQL_ADD_USER = 'INSERT INTO user2(name,password,age,sex,tel) VALUES(%s,%s,%s,%s,%s)'
    SQL_GET_PASSWORD = 'SELECT id,password,name,age,sex,tel FROM user2 WHERE password=%s'
    SQL_UPDATE_PASSWORD = 'UPDATE user2 SET password=%s WHERE id=%s'
    SQL_ACCESSLOG = 'select ip,url,status,count(*) from accesslog group by ip,url,status order by count(*) desc limit 10;'

    def __init__(self,id=None,name='',age=0,tel='',sex=1,password=''):
        self.id = id
        self.name = name
        self.age = age
        self.tel = tel
        self.sex = sex
        self.password = password

    @classmethod
    def valid_login(cls,name,password):
        args = (name,password,)
        cnt,result = DBconnection.execute_mysql(cls.SQL_LOGIN,args,one=True)
        return User(id=result[0],name=result[1],age=result[2],sex=result[3],tel=result[4]) if result else None


    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'tel': self.tel,
            'password': self.password
        }

    @classmethod
    def get_list(cls):
        cnt, result = DBconnection.execute_mysql(cls.SQL_GET_USERS)
        return [User(**dict(zip(('id', 'name', 'age', 'sex', 'tel'), line))) for line in result]

    @classmethod
    def get_by_id(cls,uid):
        cnt, result = DBconnection.execute_mysql(cls.SQL_GET_USER, (uid,), one=True)
        return User(**dict(zip(('id', 'name', 'age', 'sex', 'tel'), result)))

    @classmethod
    def get_by_name(cls,name):
        cnt, result = DBconnection.execute_mysql(cls.SQL_GET_USER_BY_NAME, (name,), one=True)
        if result:
            return User(**dict(zip(('id', 'name', 'age', 'sex', 'tel','password'), result)))

    def update(self):
        args = (self.name, self.age, self.tel, self.sex, self.id)
        cnt, result = DBconnection.execute_mysql(self.SQL_UPDATE_USER, args, fetch=False)
        return True

    @classmethod
    def delete(cls,uid):
        cnt, result = DBconnection.execute_mysql(cls.SQL_DELETE_USER, (uid,), fetch=False, curs=False)
        return True

    def add(self):
        args = (self.name, self.password, self.age, self.sex, self.tel)
        cnt, result = DBconnection.execute_mysql(self.SQL_ADD_USER, args, fetch=False, curs=False)

    def password_change(self):
        cnt, result = DBconnection.execute_mysql(self.SQL_UPDATE_PASSWORD, (self.password, self.id),fetch=False)
        return True

    @classmethod
    def accesslog_sql(cls):
        cnt, result = DBconnection.execute_mysql(cls.SQL_ACCESSLOG, fetch=True)
        result = [dict(zip(('ip', 'url', 'status', 'count(*)'), line)) for line in result]
        for i in result:
            i['count'] = i['count(*)']
        return result
