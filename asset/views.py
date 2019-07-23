from datetime import datetime
from datetime import timedelta
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from asset.models import Hosts
from django.core.exceptions import ObjectDoesNotExist
from asset.validators import asset_validators
from django.utils import timezone
from asset.models import Resources

# Create your views here.

def index(request):
    return render(request,'asset/index.html')

def list_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code':403,'result':[]})
    result = [ host.as_dict() for host in Hosts.objects.all() ]
    return JsonResponse({'code':200,'result':result})


def delete_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code': 403})
    uid = request.GET.get('uid')
    try:
        Hosts.objects.get(pk=uid).delete()
        return JsonResponse({'code': 200})
    except  ObjectDoesNotExist as e:
        return JsonResponse({'code':400,'errors':e})


def get_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code':403,'result':[]})
    uid = request.GET.get('uid')
    print(uid)
    try:
        result = Hosts.objects.get(pk=uid).as_dict()
        print(result)
        return JsonResponse({'code':200,'result':result})
    except ObjectDoesNotExist as e:
        return JsonResponse({'code':400,'errors':e})


def update_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code':403,'result':[]})
    is_valid,asset,errors = asset_validators.update_validators(request.POST)
    if is_valid:
        asset.save()
        return JsonResponse({'code':200})
    else:
        return JsonResponse({'code':400,'errors':errors})


def resource_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code':403,'result':[]})
    start_time = timezone.now() - timedelta(days=1)
    _id = request.GET.get('id')
    host = Hosts.objects.get(pk=_id)
    resources = Resources.objects.filter(ip=host.ip,created_time__gte=start_time).order_by('created_time')
    xAxis = []
    CPU_datas = []
    MEM_datas = []

    for resource in resources:
        xAxis.append(resource.created_time)
        CPU_datas.append(resource.cpu)
        MEM_datas.append(resource.mem)

    return JsonResponse({'code':200,'result':{'xAxis':xAxis,'CPU_datas':CPU_datas,'MEM_datas':MEM_datas}})