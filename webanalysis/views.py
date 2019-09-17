import os
import time
import json
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from webanalysis.models import AccessFile,AccessLog
from functools import wraps

# Create your views here.
def login_required(func):

    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('user') is None:
            if request.is_ajax():
                return JsonResponse({'code':403,'result':[]})
            return redirect('user:login')
        return func(request,*args,**kwargs)

    return wrapper


@login_required
def index(request):
    files = AccessFile.objects.filter(status=0).order_by('-created_time')[:10]
    return render(request, 'webanalysis/index.html',{'files':files})


@login_required
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


@login_required
def dist_status_code(request):
    legend,series = AccessLog.dist_status_code(request.GET.get('id',0))
    return JsonResponse({'code':200,'result':{'legend':legend,'series':series}})


@login_required
def trend_visit(request):
    xAxis, series = AccessLog.trend_visit(request.GET.get('id', 0))
    return JsonResponse({'code': 200, 'result': {'series': series, 'xAxis': xAxis}})