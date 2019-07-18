from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from asset.models import Hosts

# Create your views here.

def index(request):
    return render(request,'asset/index.html')

def list_ajax(request):
    if request.session.get('user') is None:
        redirect('user:login')
        return JsonResponse({'code':403})
    result = [ host.as_dict() for host in Hosts.objects.all() ]
    return JsonResponse({'code':200,'result':result})