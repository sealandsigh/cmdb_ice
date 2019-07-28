# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/25

import os
import json
import time
from django.conf import settings
from django.core.management import BaseCommand

class Command(BaseCommand):
    def handle(self,*args,**kwargs):
        path = os.path.join(settings.BASE_DIR, 'media', 'notices')
        while True:
            lists = os.listdir(path)
            if lists:
                for filename in lists:
                    notice = None
                    path_notice = os.path.join(path,filename)
                    with open(path_notice,'rt') as handler:
                        notice = json.loads(handler.read())

                    self.parse(notice)
                    os.unlink(path_notice)
            time.sleep(5)

    def parse(self,notice):
        print(notice)