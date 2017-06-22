# coding:utf-8
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .models import Admin_Permission

def test_perm(request):
    user = request.user
    if user.admin_permission.andriod_permisson:
        return HttpResponse('ok')
    else:
        return HttpResponse('你不是管理员'+str(user.username))


def create_admin_user(request):
    if request.method == 'POST':
        phone = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=phone,email=None,password=password)
            user.save()
            admin_permission = Admin_Permission.objects.create(user=user,andriod_permisson=True)
            admin_permission.save()
            return HttpResponseRedirect('/web/index/')
        except Exception as e:
            print e.message
            print e
            return HttpResponse('注册失败')
    return render(request, 'newadmin/index.html')


def index(request):
    return render(request, 'newadmin/index.html')


def web_login(request):
    """
    管理员登录
    :param request:
    :return:
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/web/index/')
            else:
                return HttpResponse('请输入正确的密码')
        else:
            return render(request, 'newadmin/index.html')
    else:
        return render(request,'newadmin/login.html')


def web_logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    response = HttpResponseRedirect('/web/login')
    response.delete_cookie('username')
    return response



