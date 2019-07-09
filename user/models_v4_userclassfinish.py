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
    SQL_GET_USER_BY_NAME = 'SELECT id,name,age,sex,tel FROM user2 WHERE name=%s'
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
            return User(**dict(zip(('id', 'name', 'age', 'sex', 'tel'), result)))

    @classmethod
    def valid_unique_name(cls,name,uid=None):
        user = cls.get_by_name(name)
        if uid is None:
            return not user
        else:
            if user is None:
                print('valid_name_unique is {0}'.format(user))
                return True
            else:
                return str(user.id) == str(uid)

    @classmethod
    def valid_update(cls,params):
        uid = params.get('id', '')
        name = params.get('name', '')
        tel = params.get('tel', '')
        age = params.get('age', '')
        sex = params.get('sex', '1')
        is_valid = True
        user = User()
        errors = {}

        user.id = params.get('id', '').strip()
        if get_user(user.id) is None:
            errors['uid'] = '用户信息不存在'
            is_valid = False
        user.name = params.get('name', '').strip()
        if not cls.valid_unique_name(user.name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        user.age = params.get('age', '0').strip()
        if not user.age.isdigit():
            errors['age'] = '年龄格式不正确'
            is_valid = False
        user.tel = params.get('tel', '0').strip()
        user.sex = params.get('sex', '0').strip()
        return is_valid, user, errors

    def update(self):
        args = (self.name, self.age, self.tel, self.sex, self.id)
        cnt, result = DBconnection.execute_mysql(self.SQL_UPDATE_USER, args, fetch=False)
        return True

    @classmethod
    def delete(cls,uid):
        cnt, result = DBconnection.execute_mysql(cls.SQL_DELETE_USER, (uid,), fetch=False, curs=False)
        return True

    @classmethod
    def valid_add(cls,params):
        name = params.get('name', '')
        tel = params.get('tel', '')
        age = params.get('age', '')
        sex = params.get('sex', '1')
        add_user_vaild = True
        is_valid = True
        user = User()
        errors = {}

        print(name)
        user.name = params.get('name', '').strip()
        if name == '':
            errors['name'] = '用户名输入不能为空'
            is_valid = False
        if cls.get_by_name(name):
            errors['name'] = '用户名已存在'
            is_valid = False
        user.age = params.get('age', '0').strip()
        if age == '':
            errors['name'] = '年龄不能为空'
            is_valid = False
        if not user.age.isdigit():
            errors['age'] = '年龄格式不正确'
            is_valid = False
        user.tel = params.get('tel', '0').strip()
        user.sex = params.get('sex', '0').strip()
        user.password = params.get('password', '22').strip()
        return is_valid, user, errors

    def add(self):
        args = (self.name, self.password, self.age, self.sex, self.tel)
        cnt, result = DBconnection.execute_mysql(self.SQL_ADD_USER, args, fetch=False, curs=False)

    @classmethod
    def valid_password(cls,params):
        oldpassword = params.get('oldpassword', '')
        newpassword = params.get('newpassword', '')
        newpassconfirm = params.get('newpassconfirm', '')
        uid = params.get('uid', '')
        is_valid = True
        user_password = User()
        errors = {}
        cnt, result = DBconnection.execute_mysql(SQL_GET_PASSWORD, (oldpassword,), one=True)
        result = dict(zip(('id', 'password', 'name', 'age', 'sex', 'tel'), result))

        if oldpassword == '' and result.get('password') is not None:
            is_valid = False
            errors['oldpassword'] = '旧密码不能为空请填写完整'
        if newpassword == '':
            is_valid = False
            errors['newpassword'] = '新密码不能为空请填写完整'
        if newpassconfirm == '':
            is_valid = False
            errors['newpassconfirm'] = '确认的新密码不能为空请填写完整'
        if newpassword != newpassconfirm:
            is_valid = False
            errors['passnoteq'] = '新密码两次输入不一致请重新输入'
        user_password.id = uid.strip()
        print(result.get('password'))
        user_password.password = newpassword.strip()
        return is_valid, user_password, errors, uid

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
