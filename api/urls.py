# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/12/6

from django.urls import path
#from django.urls import re_path => url
from .views import v1

app_name='api'

urlpatterns = [
    path('v1/client/<ip>/',v1.ClientView.as_view(),name='client'),
    path('v1/client/<ip>/resource/',v1.ResourceView.as_view(),name='resource')
]

