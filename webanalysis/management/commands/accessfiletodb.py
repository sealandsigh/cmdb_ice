# -*- coding: utf-8 -*-
# __author__="jiajun.zhu"
# DATE:2019/7/25

import os
import json
import time
import traceback
from datetime import datetime
from django.conf import settings
from django.core.management import BaseCommand
from webanalysis.models import AccessLog

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
                    try:
                        self.parse(notice)
                    except BaseException as e:
                        print(e)
                        print(traceback.format_exc())
                    os.unlink(path_notice)
            time.sleep(5)

    def parse(self,notice):
        print(notice)
        path = notice["path"]
        file_id = notice["id"]
        with open(path, 'rt') as fhandler:
            for line in fhandler:
                try:
                    line = line.split()
                    ip = line[0]
                    print(ip)
                    url = line[6]
                    status = line[8]
                    logtime = line[3]
                    logtime = logtime[1:]
                    logtime = datetime.strptime(logtime, '%d/%b/%Y:%H:%M:%S')
                    logtime = logtime.strftime('%Y-%m-%d %H:%M:%S')
                    print(logtime)
                    obj = AccessLog(file_id=file_id,ip=ip,url=url,status_code=status,access_time=logtime)
                    obj.save()
                except BaseException as e:
                    print(e)
                    print(line)
        print('parse over: {0}'.format(path))