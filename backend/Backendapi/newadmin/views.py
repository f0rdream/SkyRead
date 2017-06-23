# coding:utf-8
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .models import Admin_Permission,AdminBorrowItemRecord
from serializers import UserLoginSerializer,BorrowRecordSerializer,OrderRecordSerializer
from accounts.models import PhoneUser
import xlrd
def test_perm(request):
    user = request.user
    if user.admin_permission.andriod_permisson:
        return HttpResponse('ok')
    else:
        return HttpResponse('你不是管理员'+str(user.username))


def create_admin_user(request):
    """
    创建管理员
    :param request:
    :return:
    """
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


def delete_admin_user(request):
    """
    删除管理员
    :param request:
    :return:
    """
    username= request.POST['username']
    user= User.objects.get(username=username)
    user.delete()


def admin_record(request,user_id):
    """
    得到某个管理员的三个记录
    :param request:
    :return:
    """
    admin_user = User.objects.get(id=user_id)
    borrow_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=1)
    return_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=2)
    order_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=3)
    borrow_record = BorrowRecordSerializer(borrow_queryset,many=True,data={})
    return_record = BorrowRecordSerializer(return_queryset,many=True,data={})
    order_record = OrderRecordSerializer(order_queryset,many=True,data={})
    reply = {
        "borrow_record":borrow_record,
        "return_record":return_record,
        "order_record":order_record,
        "borrow_sum": len(borrow_queryset),
        "return_sum": len(return_queryset),
        "order_sum": len(order_queryset),
    }


def user_record(request,user_id):
    """
    得到某个用户的三项记录
    :param request:
    :param user_id:
    :return:
    """
    # TODO 把记录的模型加一个相关用户的字段,并在library中加入这个字段
    user = User.objects.get(id=user_id)
    about_user =user.id
    borrow_queryset = AdminBorrowItemRecord.objects.filter(record_type=1,
                                                            about_user=about_user)
    return_queryset = AdminBorrowItemRecord.objects.filter(record_type=2,
                                                           about_user=about_user)
    order_queryset = AdminBorrowItemRecord.objects.filter(record_type=3,
                                                           about_user=about_user)
    order_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user, record_type=3)
    borrow_record = BorrowRecordSerializer(borrow_queryset, many=True, data={})
    return_record = BorrowRecordSerializer(return_queryset, many=True, data={})
    order_record = OrderRecordSerializer(order_queryset, many=True, data={})
    reply = {
        "borrow_record": borrow_record,
        "return_record": return_record,
        "order_record": order_record,
        "borrow_sum": len(borrow_queryset),
        "return_sum": len(return_queryset),
        "order_sum": len(order_queryset),
    }


def day_record(request):
    """
    得到某一天的操作记录
    :param request:
    :return:
    """
    #TODO 处理时间字段以过滤


def get_user_money(request,user_id):
    """
    得到用户的金额
    :param request:
    :return:
    """
    user = User.objects.get(id=user_id)
    phone_user = PhoneUser.objects.get(user=user)
    money = phone_user.money


def add_user_money(request,user_id,sum):
    """
    增加金额,发送短信
    :param request:
    :param user_id:
    :return:
    """
    user = User.objects.get(id=user_id)
    phone_user = PhoneUser.objects.get(user=user)
    phone_user.money+=sum
    phone_user.save()


def parse_the_excel(request,url):
    """

    :param request:
    :param url:
    :return:
    """
    # TODO 用户上传文件之后得到路径
    data = xlrd.open_workbook("test.xls")












