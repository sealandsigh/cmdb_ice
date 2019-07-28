# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/25

from django.urls import path
from webanalysis import views

app_name='webanalysis'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('upload/',views.upload,name='upload'),
    path('dist_status_code/',views.dist_status_code,name='dist_status_code'),
]