import os
import time
import json
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from webanalysis.models import AccessFile

# Create your views here.
def index(request):
    return render(request, 'webanalysis/index.html')

def upload(request):
    print(request.GET)
    print(request.POST)
    log = request.FILES.get('log',None)
    if log:
        print(type(log))
        print(dir(log))
        print(log.name,log.size,log.content_type)
        path = os.path.join(settings.BASE_DIR,'media','upload',str(time.time()))
        fhandler = open(path,'wb')
        # chunks功能是django自带防止上传文件过大把内存撑破，并且上传文件类型自身也受django保护，不会撑破内存
        for chunk in log.chunks():
            fhandler.write(chunk)
        fhandler.close()

        obj = AccessFile(name=log.name,path=path)
        obj.save()

        path = os.path.join(settings.BASE_DIR,'media','notices',str(time.time()))
        with open(path,'w') as fhandler:
            fhandler.write(json.dumps({'id':obj.id,'path':obj.path}))
    return HttpResponse('upload')