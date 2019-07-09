# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/1

import traceback
from user.models import User,encrypt_password
from django.utils import timezone

class validator(object):

    @staticmethod
    def isinteger(value):
        try:
            int(value)
            return True
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
            return False

class ValidUser(validator):

    @classmethod
    def valid_login(cls, name, password):
        user = None
        try:
            user = User.objects.get(name=name)
            salt,allpassword = encrypt_password(password,user.salt)
        except BaseException as e:
            pass
        if user is None:
            return None
        if allpassword == user.password:
            return user
        return None

    @classmethod
    def valid_unique_name(cls,name,uid=None):
        user = None
        try:
            user = User.objects.get(name=name)
        except BaseException as e:
            pass
        if uid is None:
            return not user
        else:
            if user is None:
                print('valid_name_unique is {0}'.format(user))
                return True
            else:
                return str(user.id) == str(uid)

    @classmethod
    def valid_update(cls, params):
        is_valid = True
        user = None
        errors = {}
        try:
            user = User.objects.get(pk=params.get('id', '').strip())
        except BaseException as e:
            errors['uid'] = '用户信息不存在'
            is_valid = False
            return is_valid,user,errors

        name = params.get('name', '').strip()
        if name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False
        elif not cls.valid_unique_name(name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        else:
            user.name = name
        age = params.get('age', '0').strip()
        if not cls.isinteger(age):
            errors['age'] = '年龄格式不正确'
            is_valid = False
        else:
            user.age = int(age)
        user.tel = params.get('tel', '0').strip()
        user.sex = params.get('sex', '0').strip()
        return is_valid, user, errors

    @classmethod
    def valid_add(cls, params):
        name = params.get('name', '')
        tel = params.get('tel', '')
        age = params.get('age', '')
        sex = params.get('sex', '1')
        add_user_vaild = True
        is_valid = True
        user = User()
        errors = {}

        user.name = params.get('name', '').strip()
        if name == '':
            errors['name'] = '用户名输入不能为空'
            is_valid = False
        else:
            try:
                User.objects.get(name=name)
                errors['name'] = '用户名已存在'
                is_valid = False
            except BaseException as e:
                pass
        user.age = params.get('age', '0').strip()
        if age == '':
            errors['name'] = '年龄不能为空'
            is_valid = False
        if not cls.isinteger(user.age):
            errors['age'] = '年龄格式不正确'
            is_valid = False
        else:
            user.age = int(user.age)
        user.tel = params.get('tel', '0').strip()
        user.sex = params.get('sex', '0').strip()
        salt,allpassword = encrypt_password(params.get('password', '22').strip())
        # user.password = params.get('password', '22').strip()
        user.salt = salt
        user.password = allpassword
        user.create_time = timezone.now()
        return is_valid, user, errors

    @classmethod
    def valid_password(cls, params):
        oldpassword = params.get('oldpassword', '')
        newpassword = params.get('newpassword', '')
        newpassconfirm = params.get('newpassconfirm', '')
        uid = params.get('uid', '')
        is_valid = True
        user_password = User.objects.get(pk=uid)
        salt, allpassword = encrypt_password(oldpassword,user_password.salt)
        errors = {}
        result = user_password.password

        if oldpassword == '' and result is not None:
            is_valid = False
            errors['oldpassword'] = '旧密码不能为空请填写完整'
        if result != allpassword:
            is_valid = False
            errors['oldpassword'] = '旧密码输入错误'
        if newpassword == '':
            is_valid = False
            errors['newpassword'] = '新密码不能为空请填写完整'
        if newpassconfirm == '':
            is_valid = False
            errors['newpassconfirm'] = '确认的新密码不能为空请填写完整'
        if newpassword != newpassconfirm:
            is_valid = False
            errors['passnoteq'] = '新密码两次输入不一致请重新输入'
        salt,allpassword = encrypt_password(newpassword)
        user_password.password = allpassword
        user_password.salt = salt
        return is_valid, user_password, errors, uid