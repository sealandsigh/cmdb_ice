# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/19

from asset.models import Hosts
from django.core.exceptions import ObjectDoesNotExist

class asset_validators():

    @classmethod
    def update_validators(cls,params):
        is_valid = True
        asset = None
        errors = {}

        try:
            asset = Hosts.objects.get(pk=params.get('id','').strip())
        except ObjectDoesNotExist as e:
            is_valid = False
            errors['id'] = '用户不存在'
            return is_valid,errors

        name = params.get('name','').strip()
        if name == '':
            is_valid = False
            errors['name'] = '主机名不能为空'
            return is_valid,errors
        else:
            asset.name = name
            print("assetname:{0}".format(asset.name))

        return is_valid,asset,errors