from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from asset.models import Hosts
from django.core.exceptions import ObjectDoesNotExist
from asset.validators import asset_validators

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