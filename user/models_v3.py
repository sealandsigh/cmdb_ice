#encoding: utf-8

import json
import MySQLdb

from MySQLdb import cursors
from .dbutils import DBconnection
from django.db import models

# Create your models here.
DATA_FILE = 'user.data.json'

SQL_LOGIN = 'select id,name,age,sex,tel from user2 where name=%s and password=%s limit 1'
SQL_GET_USERS = 'select id,name,age,sex,tel from user2'
SQL_GET_USER = 'SELECT id,name,age,sex,tel FROM user2 WHERE id=%s'
SQL_GET_USER_BY_NAME = 'SELECT id,name,age,sex,tel FROM user2 WHERE name=%s'
SQL_UPDATE_USER = 'UPDATE user2 SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s'
SQL_ADD_USER = 'INSERT INTO user2(name,password,age,sex,tel) VALUES(%s,%s,%s,%s,%s)'
SQL_DELETE_USER = 'DELETE FROM user2 WHERE id=%s'
SQL_GET_PASSWORD = 'SELECT id,password,name,age,sex,tel FROM user2 WHERE password=%s'
SQL_UPDATE_PASSWORD = 'UPDATE user2 SET password=%s WHERE id=%s'
SQL_ACCESSLOG = 'select ip,url,status,count(*) from accesslog group by ip,url,status order by count(*) desc limit 10;'

def get_users():
    cnt,result = DBconnection.execute_mysql(SQL_GET_USERS)
    # return result
    return [dict(zip(('id','name','age','sex','tel'),line)) for line in result]

def dump_users(users):
    fhandler = open(DATA_FILE,'wt')
    fhandler.write(json.dumps(users))
    fhandler.close()
    return True


def valid_login(name,password):
    cnt, result = DBconnection.execute_mysql(SQL_LOGIN,(name,password),one=True,curs=False)
    return {'id':result[0],'name':result[1]} if result else None


def delete_user(uid):
    cnt, result = DBconnection.execute_mysql(SQL_DELETE_USER,(uid,),fetch=False, curs=False)
    return True

def get_user(uid):
    cnt, result = DBconnection.execute_mysql(SQL_GET_USER, (uid,),one=True)
    return dict(zip(('id', 'name', 'age', 'sex', 'tel'), result))

def valid_get_user_by_name(name):
    cnt, result = DBconnection.execute_mysql(SQL_GET_USER_BY_NAME, (name,), one=True)
    if result:
        return dict(zip(('id', 'name', 'age', 'sex', 'tel'), result))

def valid_name_unique(name,uid=None):
    user = valid_get_user_by_name(name)
    if uid is None:
        return not user
    else:
        if user is None:
            print('valid_name_unique is {0}'.format(user))
            return True
        else:
            return str(user['id']) == str(uid)


def valid_update_user(params):
    uid = params.get('id','')
    name = params.get('name','')
    tel = params.get('tel','')
    age = params.get('age','')
    sex = params.get('sex','1')
    is_valid = True
    user = {}
    errors = {}

    user['id'] = params.get('id', '').strip()
    if get_user(user['id']) is None:
        errors['uid'] = '用户信息不存在'
        is_valid = False
    user['name'] = params.get('name','').strip()
    print(valid_name_unique(user['name'],user['id']))
    if not valid_name_unique(user['name'],user['id']):
            errors['name'] = '用户名已存在'
            is_valid = False
    user['age'] = params.get('age','0').strip()
    if not user['age'].isdigit():
        errors['age'] = '年龄格式不正确'
        is_valid = False
    user['tel'] = params.get('tel','0').strip()
    user['sex'] = params.get('sex','0').strip()
    return is_valid,user,errors


def update_user(params):
    args = (params['name'],params['age'],params['tel'],params['sex'],params['id'])
    cnt, result = DBconnection.execute_mysql(SQL_UPDATE_USER, args, fetch=False)
    return True


def valid_add_user(params):
    name = params.get('name', '')
    tel = params.get('tel', '')
    age = params.get('age', '')
    sex = params.get('sex', '1')
    add_user_vaild = True
    is_valid = True
    user = {}
    errors = {}

    print(name)
    user['name'] = params.get('name', '').strip()
    if name == '':
        errors['name'] = '用户名输入不能为空'
        is_valid = False
    if valid_get_user_by_name(name):
        errors['name'] = '用户名已存在'
        is_valid = False
    user['age'] = params.get('age','0').strip()
    if age == '':
        errors['name'] = '年龄不能为空'
        is_valid = False
    if not user['age'].isdigit():
        errors['age'] = '年龄格式不正确'
        is_valid = False
    user['tel'] = params.get('tel','0').strip()
    user['sex'] = params.get('sex','0').strip()
    user['password'] = params.get('password', '22').strip()
    return is_valid, user, errors


def add_user(params):
    args = (params['name'],params['password'],params['age'],params['sex'],params['tel'])
    cnt, result = DBconnection.execute_mysql(SQL_ADD_USER, args, fetch=False,curs=False)


def valid_password_user(params):
    oldpassword = params.get('oldpassword','')
    newpassword = params.get('newpassword','')
    newpassconfirm = params.get('newpassconfirm','')
    uid = params.get('uid','')
    is_valid = True
    user_password = {}
    errors = {}
    cnt, result = DBconnection.execute_mysql(SQL_GET_PASSWORD,(oldpassword,),one=True)
    result = dict(zip(('id','password','name','age','sex','tel'),result))
    print('nihao')
    print(result)

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
    user_password['uid'] = uid.strip()
    print(result.get('password'))
    user_password['newpassword'] = newpassword.strip()
    return is_valid,user_password,errors,uid


def change_password(params):
    cnt, result = DBconnection.execute_mysql(SQL_UPDATE_PASSWORD, (params['newpassword'],params['uid']),fetch=False)
    return True


def sql_accesslog():
    cnt, result = DBconnection.execute_mysql(SQL_ACCESSLOG, fetch=True)
    result = [dict(zip(('ip','url','status','count(*)'),line)) for line in result]
    for i in result:
        i['count'] = i['count(*)']
    return result