#encoding: utf-8

import json
from django.db import models

# Create your models here.
DATA_FILE = 'user.data.json'

def get_users():
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
    users = get_users()
    for uid, user in users.items():
        if user['name'] == name and user['password'] == password:
            user['id'] = uid
            return user
    return None


def delete_user(uid):
    users = get_users()
    users.pop(uid,None)
    dump_users(users)
    return True


def get_user(uid):
    users = get_users()
    user = users.get(uid,{})
    user['id'] = uid
    return user


def valid_update_user(params):
    uid = params.get('id','')
    name = params.get('name','')
    tel = params.get('tel','')
    age = params.get('age','')
    sex = params.get('sex','1')
    is_valid = True
    user = {}
    errors = {}
    users = get_users()

    user['id'] = params.get('id', '').strip()
    if users.get(user['id']) is None:
        errors['uid'] = '用户信息不存在'
        is_valid = False
    user['name'] = params.get('name','').strip()
    for uid,cuser in users.items():
        if cuser['name'] == user['name'] and uid != user['id']:
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
    uid = params.pop('id')
    users = get_users()
    users[uid].update(params)
    return dump_users(users)


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
    for uid, cuser in users.items():
        if cuser['name'] == user['name']:
            errors['name'] = '用户名已存在'
            is_valid = False
    user['age'] = params.get('age','0').strip()
    if not user['age'][0].isdigit():
        errors['age'] = '年龄格式不正确'
        is_valid = False
    user['tel'] = params.get('tel','0').strip()
    user['sex'] = params.get('sex','0').strip()
    return is_valid, user, errors


def add_user(params):
    users = get_users()
    uid = int(max(users)) + 1
    users[str(uid)] = params
    return dump_users(users)


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