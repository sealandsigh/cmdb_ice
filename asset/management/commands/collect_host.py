# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/15

from django.core.management import BaseCommand

class Command(BaseCommand):

    def handle(self,*args,**options):
        print('test')