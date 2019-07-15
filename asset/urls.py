# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/15

from django.urls import path
from asset import views

app_name='asset'

urlpatterns = [
    path('',views.index,name='index'),
]