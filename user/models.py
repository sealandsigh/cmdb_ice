#encoding: utf-8

import hashlib
import random
from django.db import models
from .dbutils import DBconnection

# Create your models here.
def encrypt_password(password,salt=None):
    seed = 'zhujiajun'
    sa = []
    for i in range(8):
        sa.append(random.choice(seed))
    if salt:
        salt = salt
    else:
        salt = ''.join(sa)
        md5 = hashlib.md5()
        md5.update(salt.encode())
        salt = md5.hexdigest()
    passwordmd5 = hashlib.md5()
    allpassword = salt + str(password)
    passwordmd5.update(allpassword.encode())
    allpassword = passwordmd5.hexdigest()
    return salt,allpassword

class User(models.Model):
    name = models.CharField(max_length=32,null=False,default='')
    password = models.CharField(max_length=512,null=False,default='')
    age = models.IntegerField(null=False,default=0)
    tel = models.CharField(max_length=32,null=False,default='')
    sex = models.BooleanField(null=False,default=True)
    create_time = models.DateTimeField(null=False)
    addr = models.CharField(max_length=120,null=False,default='')
    salt = models.CharField(max_length=512,null=False,default='')

    @staticmethod
    def accesslog_sql():
        SQL_ACCESSLOG = '''
                           select ip,url,status,count(*) from accesslog 
                           group by ip,url,status 
                           order by count(*) desc limit 10;
                           '''
        cnt, result = DBconnection.execute_mysql(SQL_ACCESSLOG, fetch=True)
        result = [dict(zip(('ip', 'url', 'status', 'count(*)'), line)) for line in result]
        for i in result:
            i['count'] = i['count(*)']
        return result

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'sex': self.sex,
            'tel': self.tel,
            'password': self.password
        }
