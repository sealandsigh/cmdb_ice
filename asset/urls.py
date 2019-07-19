# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/15

from django.urls import path
from asset import views

app_name='asset'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('list/ajax/',views.list_ajax,name='list_ajax'),
    path('delete/ajax/',views.delete_ajax,name='delete_ajax'),
    path('get/ajax/',views.get_ajax,name='get_ajax'),
    path('update/ajax/',views.update_ajax,name='update_ajax'),
]