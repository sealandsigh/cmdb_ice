# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/12/6

from django.views.generic import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

class ClientView(View):

    def get(self,request,*arge,**kwargs):
        print(request.GET)
        print(request.POST)
        print(request.body)
        print(arge,kwargs)
        return HttpResponse('get ok')

    @csrf_exempt
    def dispatch(self,request,*args,**kwargs):
        return super(ClientView,self).dispatch(request,*args,**kwargs)

    def post(self,request,*args,**kwargs):
        print(request.GET)
        print(request.POST)
        print(request.body)
        print(args,kwargs)
        return HttpResponse('post ok')