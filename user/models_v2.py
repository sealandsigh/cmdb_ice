#encoding: utf-8

import json
import MySQLdb

from MySQLdb import cursors
from django.db import models

# Create your models here.
DATA_FILE = 'user.data.json'

MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWD = 'zhujiajun'
MYSQL_DB = 'zhujiajun'
MYSQL_CHARSET = 'utf8'
SQL_LOGIN = 'select id,name,age,sex,tel from user2 where name=%s and password=%s limit 1'
SQL_GET_USERS = 'select id,name,age,sex,tel from user2'
SQL_GET_USER = 'SELECT id,name,age,sex,tel FROM user2 WHERE id=%s'
SQL_GET_USER_BY_NAME = 'SELECT id,name,age,sex,tel FROM user2 WHERE name=%s'
SQL_UPDATE_USER = 'UPDATE user2 SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s'
SQL_ADD_USER = 'INSERT INTO user2(name,password,age,sex,tel) VALUES(%s,%s,%s,%s,%s)'
SQL_DELETE_USER = 'DELETE FROM user2 WHERE id=%s'


def get_users():
    conn = MySQLdb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,
                           passwd=MYSQL_PASSWD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_GET_USERS)
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
    fhandler = open(DATA_FILE,'rt')
    users = json.loads(fhandler.read())
    fhandler.close()
    return users


def dump_users(users):
    fhandler = open(DATA_FILE,'wt')
    fhandler.write(json.dumps(users))
    fhandler.close()
    return True


def valid_login(name,password):
    conn = MySQLdb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,
                           passwd=MYSQL_PASSWD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor()
    cur.execute(SQL_LOGIN,(name,password))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return {'id':result[0],'name':result[1]} if result else None
    # users = get_users()
    # for uid, user in users.items():
    #     if user['name'] == name and user['password'] == password:
    #         user['id'] = uid
    #         return user
    # return None


def delete_user(uid):
    conn = MySQLdb.connect(host=MYSQL_HOST,port=MYSQL_PORT,user=MYSQL_USER,
                           passwd=MYSQL_PASSWD,db=MYSQL_DB,charset=MYSQL_CHARSET)
    cur = conn.cursor()
    cur.execute(SQL_DELETE_USER,(uid,))
    conn.commit()
    cur.close()
    conn.close()
    return True
    # users = get_users()
    # users.pop(uid,None)
    # dump_users(users)
    # return True


def get_user(uid):
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                           passwd=MYSQL_PASSWD, db=MYSQL_DB, charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_GET_USER, (uid,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result
    # users = get_users()
    # user = users.get(uid,{})
    # user['id'] = uid
    # return user


def valid_get_user_by_name(name):
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                           passwd=MYSQL_PASSWD, db=MYSQL_DB, charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_GET_USER_BY_NAME, (name,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result


def valid_name_unique(name,uid=None):
    user = valid_get_user_by_name(name)
    if uid is None:
        return not user
    else:
        if user is None:
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
    # users = get_users()

    user['id'] = params.get('id', '').strip()
    if get_user(user['id']) is None:
        errors['uid'] = '用户信息不存在'
        is_valid = False
    user['name'] = params.get('name','').strip()
    print(valid_name_unique(user['name'],user['id']))
    if not valid_name_unique(user['name'],user['id']):
    # for uid,cuser in users.items():
    #     if cuser['name'] == user['name'] and uid != user['id']:
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
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                           passwd=MYSQL_PASSWD, db=MYSQL_DB, charset=MYSQL_CHARSET)
    cur = conn.cursor(cursors.DictCursor)
    cur.execute(SQL_UPDATE_USER, (params['name'],params['age'],params['tel'],params['sex'],params['id']))
    conn.commit()
    cur.close()
    conn.close()
    return True
    # uid = params.pop('id')
    # users = get_users()
    # users[uid].update(params)
    # return dump_users(users)


def valid_add_user(params):
    name = params.get('name', '')
    tel = params.get('tel', '')
    age = params.get('age', '')
    sex = params.get('sex', '1')
    add_user_vaild = True
    is_valid = True
    user = {}
    errors = {}
    users = get_users()

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
    print(params['name'],params['password'],params['age'],params['sex'],params['tel'])
    conn = MySQLdb.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER,
                           passwd=MYSQL_PASSWD, db=MYSQL_DB, charset=MYSQL_CHARSET)
    cur = conn.cursor()
    zhixing = cur.execute(SQL_ADD_USER,(params['name'],params['password'],params['age'],params['sex'],params['tel']))
    print(SQL_ADD_USER,(params['name'],params['password'],params['age'],params['sex'],params['tel']))
    conn.commit()
    cur.close()
    conn.close()
    return True
    # users = get_users()
    # uid = int(max(users)) + 1
    # users[str(uid)] = params
    # return dump_users(users)


def valid_password_user(params):
    oldpassword = params.get('oldpassword','')
    newpassword = params.get('newpassword','')
    newpassconfirm = params.get('newpassconfirm','')
    uid = params.get('uid','')
    is_valid = True
    user_password = {}
    errors = {}
    users = get_users()

    if oldpassword == '' and users[uid].get('password') is not None:
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
    print(users[uid].get('password'))
    user_password['newpassword'] = newpassword.strip()
    return is_valid,user_password,errors,uid


def change_password(params):
    users = get_users()
    uid = params['uid']
    newpassword = params['newpassword']
    users[uid]['password'] = newpassword
    return dump_users(users)