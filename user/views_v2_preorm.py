# encoding: utf-8
from django.shortcuts import render,redirect
from user.models import User
from user.validators import ValidUser
from django.http import HttpResponse
# Create your views here.
def index(request):
    if not request.session.get('user'):
        return redirect('user:login')
    return render(request,'user/test.html',{
                   # 'users':get_users()
                   'users':User.get_list()
    })
    #return HttpResponse('我的第一个网页')


def login(request):
    if request.method == 'GET':
        return render(request,'user/login.html')
    elif request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        user = ValidUser.valid_login(name,password)
        if user:
            request.session['user'] = user.as_dict()
            return redirect('user:index')
        else:
            return render(request,'user/login.html',{
                'name':name,
                'password':password,
                'errors':{'default':'用户名或密码错误'}
            })


def logout(request):
    request.session.flush()
    return redirect('user:login')


def delete(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    uid = request.GET.get('uid')
    User.delete(uid)
    return redirect('user:index')


def view(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    uid = request.GET.get('uid')
    return render(request,'user/view.html',{'user':User.get_by_id(uid)})


def update(request):
    if request.session.get('user') is None:
        return redirect('user:login')

    is_valid,user,errors = ValidUser.valid_update(request.POST)
    if is_valid:
        user.update()
        return redirect('user:index')
    else:
        return render(request,'user/view.html',{
            'user':user,
            'errors':errors
        })


def addview(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    return render(request,'user/add.html')

def add(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    add_user_vaild,user,errors = ValidUser.valid_add(request.POST)
    print(add_user_vaild)
    if add_user_vaild:
        user.add()
        return redirect('user:index')
    else:
        return render(request,'user/add.html',{
            'user':user,
            'errors':errors
        })


def passwordview(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    uid = request.GET.get('uid')
    return render(request,'user/password.html',{'uid':uid})


def password(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    is_valid,user_password,errors,uid = ValidUser.valid_password(request.POST)
    if is_valid:
        user_password.password_change()
        return redirect('user:index')
    else:
        return render(request,'user/password.html',{
            'uid':uid,
            'errors':errors
        })


def accesslog(request):
    if request.session.get('user') is None:
        return redirect('user:login')
    return render(request,'user/accesslog.html',{
        'accesslog':User.accesslog_sql()
    })