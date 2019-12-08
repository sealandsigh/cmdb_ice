# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/12/6

import json

from django.views.generic import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from asset.models import Hosts,Resources

class ApiView(View):

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(ApiView, self).dispatch(request, *args, **kwargs)

    def get_json(self):
        try:
            return json.loads(self.request.body)
        except BaseException as e:
            return {}

    def response(self,result=None,code=200,errors={}):
        return JsonResponse({'code': 200, 'result': None, 'errors': {}})

class ClientView(ApiView):

    def post(self,request,*args,**kwargs):
        _ip = kwargs.get('ip','')
        _json = self.get_json()

        host = Hosts.create_or_replace(_json.get('name',''), \
                                       _ip,\
                                       _json.get('mac',''), \
                                       _json.get('os',''),\
                                       _json.get('arch',''),\
                                       _json.get('mem',0),\
                                       _json.get('cpu',0),\
                                       _json.get('disk','{}'))
        return self.response(host.as_dict())

class ResourceView(ApiView):

    def post(self,request,*args,**kwargs):
        _ip = kwargs.get('ip', '')
        _json = self.get_json()

        Resources.create_obj(_ip,_json.get('cpu',0),_json.get('mem',0))
        return self.response()