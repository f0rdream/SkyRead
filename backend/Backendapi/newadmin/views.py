# coding:utf-8
import time
import xlwt
from django.contrib.auth.models import User, Permission
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.contrib.auth import login, authenticate,logout
from .models import Admin_Permission,AdminBorrowItemRecord,ExcelFile,Sign
from serializers import UserLoginSerializer,BorrowRecordSerializer,OrderRecordSerializer
from accounts.models import PhoneUser,WeChatUser
from bookdata.models import Book,Holding
from django.db import connection
from bookdata.models import Holding
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from library.models import BorrowItem,SuccessOrderItem,WaitOrderItem
from models import Picture
from send_message import send_borrow_message,send_back_wechat
from accounts.models import FeedBack


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
                print "yes"
                return HttpResponseRedirect('/web/index/')
            else:
                return HttpResponse('请输入正确的密码')
        else:
            print "no"
            return render(request,'newadmin/login.html')
    else:
        print "?"
        return render(request,'newadmin/login.html')


def web_logout(request):
    """
    退出登录
    :param request:
    :return:
    """
    response = HttpResponseRedirect('/web/login')
    logout(request)
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


def user_detail(request,id):
    """
    得到某个用户的三项记录
    :param request:
    :param user_id:
    :return:
    """
    # TODO 把记录的模型加一个相关用户的字段,并在library中加入这个字段
    wechat_user = WeChatUser.objects.get(id=id)
    open_id = wechat_user.openid
    user = User.objects.get(username=open_id)
    borrow_record = BorrowItem.objects.filter(user=user,in_return_bar=True,finish_return=False)
    return_record = BorrowItem.objects.filter(user=user,finish_return=True)
    order_success_record = SuccessOrderItem.objects.filter(user=user)
    order_wait_record = WaitOrderItem.objects.filter(user=user)
    borrow_sum = len(borrow_record)
    return_sum = len(return_record)
    success_sum = len(order_success_record)
    wait_sum = len(order_wait_record)
    reply = {
        "wechat_user":wechat_user,
        "borrow_record": borrow_record,
        "return_record": return_record,
        "order_success_record": order_success_record,
        "order_wait_record":order_wait_record,
        "borrow_sum": borrow_sum,
        "return_sum": return_sum,
        "order_success_sum":success_sum,
        "order_wait_sum": wait_sum,
        "username": request.user.username,
        'active_class': 2
    }
    return render(request,"newadmin/user_detail.html",reply)


def day_record(request):
    """
    得到某一天的操作记录
    :param request:
    :return:
    """
    # TODO 处理时间字段以过滤


def get_user_money(request,user_id):
    """
    得到用户的金额
    :param request:
    :return:
    """
    user = User.objects.get(id=user_id)
    phone_user = PhoneUser.objects.get(user=user)
    money = phone_user.money


def add_user_money(request):
    """
    增加金额,发送短信
    :param request:
    :param user_id:
    :return:
    """

    user = User.objects.get(id=user_id)
    phone_user = PhoneUser.objects.get(user=user)
    phone_user.money += sum
    phone_user.save()


def parse_the_excel(request):
    """
    :param request:
    :param url:
    :return:
    """
    # TODO 用户上传文件之后得到路径
    url = "/media_root/newadmin/upload/model.xls"
    file_name = url.split("/")[-1]
    new_url = "./media_root/newadmin/upload/"+file_name
    print new_url
    curBook = xlrd.open_workbook(new_url)
    sheet1 = curBook.sheet_by_index(0)
    rownum = sheet1.nrows
    colnum = sheet1.ncols
    for i in range(1,rownum):
        isbn13 = str('{:.0f}'.format(sheet1.cell(i,0).value))
        find_id = str(sheet1.cell(i,1).value)
        location = str(sheet1.cell(i,2).value)
        if isbn13=='978712345678':
            print "get all "
        print isbn13
        print find_id
        print location
    return HttpResponse("get")


def add_book_excel(request):
    if request.method == 'POST':
        excel = request.FILES['excel']
        try:
            excel_file = ExcelFile.objects.create(excel=excel)
            excel_file.save()
            # 开始读取excel
            url = excel_file.excel.url
            file_name = url.split("/")[-1]
            new_url = "./media_root/newadmin/upload/" + file_name
            print new_url
            curBook = xlrd.open_workbook(new_url)
            sheet1 = curBook.sheet_by_index(0)
            rownum = sheet1.nrows
            holdings = list()
            for i in range(1, rownum):
                isbn13 = str(sheet1.cell(i, 0).value)
                find_id = str(sheet1.cell(i, 1).value)
                location = str(sheet1.cell(i, 2).value)
                try:
                    book = Book.objects.get(isbn13=isbn13)
                    holding = Holding.objects.create(book=book, isbn13=isbn13,
                                                     find_id=find_id, location=location,
                                                        back_time = "--")
                    holding.save()
                    holdings.append(holding)
                except:
                    pass
            reply = {
                "holdings":holdings,
                "msg":"添加成功,书籍信息如下",
                "username": request.user.username,
                'active_class': 3
            }
            return render(request,"newadmin/add_book_by_excel_success.html",reply)
        except Exception as e:
            print e
            print e.message
            reply = {
                "msg": "添加失败",
                "username": request.user.username,
                'active_class': 3
            }
            return render(request, "newadmin/add_book_by_excel_success.html", reply)
    reply = {
        "msg": "添加失败",
        "username": request.user.username
    }
    return render(request, "newadmin/add_book_by_excel.html", reply)


def add_single_book(request):
    if request.method == "POST":
        isbn13 = request.POST['isbn13']
        find_id = request.POST['find_id']
        location = request.POST['location']
        try:
            book = Book.objects.get(isbn13=isbn13)
            holding = Holding.objects.create(book=book,isbn13=isbn13,
                                             find_id=find_id,location=location,back_time="--")
            holding.save()
            reply = {
                "msg":"添加成功,添加的信息如下:",
                "holding":holding,
                "username": request.user.username,
                'active_class': 3
            }
            return render(request, 'newadmin/add_book_success.html',reply)
        except Exception as e :
            print e
            reply = {
                "msg": "添加失败",
                "username": request.user.username,
                'active_class': 3
            }
            return render(request, 'newadmin/add_book_success.html', reply)
    else:
        return render(request,"newadmin/index.html")


def adminer_home(request):
    user_list = User.objects.all()
    admin_user_list = list()
    reply = dict()
    all_signs = list()
    if request.user.is_authenticated():
        for user in user_list:
            if user.admin_permission.andriod_permisson and not\
                    user.admin_permission.admin_permisson:
                try:
                    sign = Sign.objects.get(user=user)
                    all_signs.append(sign)
                    admin_detail = {
                        'username': user.username,
                        'sign_times': sign.times,
                        'active_class': 1
                    }
                    reply[user.id] = admin_detail
                except:
                    admin_detail = {
                        'username': user.username,
                        'sign_times': 0,
                        'active_class': 1
                    }
                    reply[user.id] = admin_detail
        return render(request,'newadmin/adminer.html',{'reply':reply,"signs":all_signs,
                                                       "username":request.user.username})
    else:
        return render(request, 'newadmin/login.html')


def adminer_detail(request,user_id):
    """
    得到某个管理员的三个记录
    :param request:
    :return:
    """
    admin_user = User.objects.get(id=user_id)
    borrow_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=1)
    return_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=2)
    order_queryset = AdminBorrowItemRecord.objects.filter(user=admin_user,record_type=3)
    reply = {
        "borrow_record":borrow_queryset,
        "return_record":return_queryset,
        "order_record":order_queryset,
        "borrow_sum": len(borrow_queryset),
        "return_sum": len(return_queryset),
        "order_sum": len(order_queryset),
        "username": request.user.username,
        'active_class': 1
    }
    return render(request, 'newadmin/adminer_detail.html',reply)


def money_home(request):
    phone_user_list = PhoneUser.objects.all()
    reply = {
        'phone_users':phone_user_list
    }
    return render(request,"newadmin/money_home.html",reply)


def book_home(request):
    import time
    begin = time.time()
    # 取前20本书籍
    cursor = connection.cursor()
    sql = "select isbn13 from bookdata_book where average > 9.0 and numraters >200 limit 0,20"
    cursor.execute(sql)
    rs = cursor.fetchall()
    all_book_list = list()
    for row in rs:
        isbn13 = row[0]
        all_book_list.append(isbn13)
    book_items = Book.objects.filter(isbn13__in=all_book_list)
    reply  = {
        "book_items":book_items,
        "page":1,
        "username": request.user.username,
        "total_page": 200000,
        'active_class': 3
    }
    print time.time() - begin
    return render(request, "newadmin/book_home.html",reply)


def book_home_change_page(request, back_page):
    """
    图书主页分页功能
    :param request:
    :return:
    """
    back_page = int(back_page)
    if back_page <= 1:
        cursor = connection.cursor()
        sql = "select isbn13 from bookdata_book where average > 9.0 and numraters >200 limit 0,20"
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_book_list = list()
        for row in rs:
            isbn13 = row[0]
            all_book_list.append(isbn13)
        book_items = Book.objects.filter(isbn13__in=all_book_list)
        reply = {
            "book_items":book_items,
            "page": 1,
            "username": request.user.username,
            "total_page": 200000,
            'active_class': 1
        }
        return render(request,'newadmin/book_home.html',reply)
    else:
        cursor = connection.cursor()
        sql = "select isbn13 from bookdata_book where average > 9.0  " \
              "and numraters >200 limit %s,%s" %((back_page-1)*20,20)
        cursor.execute(sql)
        rs = cursor.fetchall()
        all_book_list = list()
        for row in rs:
            isbn13 = row[0]
            all_book_list.append(isbn13)
        book_items = Book.objects.filter(isbn13__in=all_book_list)
        reply = {
            "book_items": book_items,
            "page": back_page,
            "username": request.user.username,
            "total_page": 200000,
            'active_class': 1
        }
        return render(request, 'newadmin/book_home.html', reply)


def book_search(request):
    """
    书籍搜索
    :param request:
    :return:
    """
    try:
        isbn13 = request.POST['isbn13']
        book_name = request.POST['book_name']
        queryset = Book.objects.all()
        isbn13_queryset = list()
        title_queryset = list()
        begin = time.time()
        if isbn13:
            queryset = queryset.filter(isbn13=isbn13)
            for book in queryset:
                isbn13_queryset.append(book)
        if book_name:
            from django.db import connection
            cursor = connection.cursor()
            text_index = ''
            for i in book_name:
                sql = "select number from bookinfo.char_number where title='%s'" % i
                cursor.execute(sql)
                rs = cursor.fetchall()
                for row in rs:
                    number = row[0]
                    text_index += '&'
                    text_index += number
            select_sql = "select isbn13 from bookdata_book where match (title_for_index)\
              against ('+%s' in boolean mode) order by average desc limit 15;" % text_index
            cursor.execute(select_sql)
            title_rs = cursor.fetchall()
            isbn13_list = []
            for row in title_rs:
                isbn13 = row[0]
                isbn13_list.append(isbn13)
            for isbn13 in isbn13_list:
                book = Book.objects.get(isbn13=isbn13)
                title_queryset.append(book)
        book_items = isbn13_queryset+title_queryset
        reply = {
            "book_items": book_items,
            "page": 1,
            "username": request.user.username,
            'active_class': 3
        }
        print time.time()-begin
        return render(request, 'newadmin/search.html', reply)
    except:
        book_items = Book.objects.all()[20:40]
        reply = {
            "book_items": book_items,
            "page": 1,
            "username": request.user.username,
            'active_class': 3
        }
        return render(request, "newadmin/search.html", reply)


def book_detail(request,isbn13):
    """
    书籍详情
    :param request:
    :param isbn13:
    :return:
    """
    book = Book.objects.get(isbn13=isbn13)
    holding_queryset = Holding.objects.filter(book=book)
    for holding in holding_queryset:
        location = holding.location
        try:
            l_loaction = ['总馆', '信息馆', '工学馆', '医学馆']
            guide = ['东', '西', '南', '北']
            location_list = location.split("->")
            real_location = l_loaction[int(location_list[0])] + "借阅区" + str(location_list[1]) + \
                            "楼" + guide[int(location_list[2])]
            holding.location = real_location
        except:
            holding.location = holding.location
    reply = {
        'book':book,
        'holdings':holding_queryset,
        "username": request.user.username,
        'active_class': 3
    }
    return render(request,"newadmin/book_detail.html",reply)


def user_home(request):
    """
    用户主页
    :param request:
    :return:
    """
    all_wechat_user = WeChatUser.objects.all()
    reply = {
        "wechat_users":all_wechat_user,
        "username": request.user.username,
        'active_class': 2
    }
    return render(request,"newadmin/user_home.html",reply)


def user_record(request,id):
    all_user = User.objects.all()
    wechat_list = list()
    reply_json = dict()
    count = 0
    for user in all_user:
        if not user.admin_permission.andriod_permisson:
            count += 1
            wechat_list.append(user)
            about_user = user.id
            borrow_queryset = AdminBorrowItemRecord.objects.filter(record_type=1,
                                                                   about_user=about_user)
            return_queryset = AdminBorrowItemRecord.objects.filter(record_type=2,
                                                                   about_user=about_user)
            order_queryset = AdminBorrowItemRecord.objects.filter(record_type=3,
                                                                  about_user=about_user)
            borrow_record = BorrowRecordSerializer(borrow_queryset, many=True, data={})
            return_record = BorrowRecordSerializer(return_queryset, many=True, data={})
            order_record = OrderRecordSerializer(order_queryset, many=True, data={})
            # TODO 添加用户微信信息
            username = user.username
            reply = {
                "borrow_record": borrow_record,
                "return_record": return_record,
                "order_record": order_record,
                "borrow_sum": len(borrow_queryset),
                "return_sum": len(return_queryset),
                "order_sum": len(order_queryset),
                "username": request.user.username,
            }
            reply_json[str(count)] = reply
    print type(wechat_list)
    return render(request, 'newadmin/user_detail.html',{'reply':reply_json})


def file_download(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=model.xls'
    workbook = xlwt.Workbook(encoding='utf-8')  # 创建工作簿
    sheet = workbook.add_sheet("sheet1")  # 创建工作页
    row0 = [u'isbn13', u'索书号', u'馆藏信息']
    for i in range(0, len(row0)):
        sheet.write(0, i, row0[i])
    workbook.save(response)
    return response


def add_picture(request):
    if request.method == 'POST':
        picture = request.FILES['picture']
        title = request.POST['title']
        isbn13 = request.POST['isbn13']
        try:
            about_book = Book.objects.get(isbn13=isbn13)
            new_picture = Picture.objects.create(picture=picture, title=title,
                                                 isbn13=isbn13, about_book=about_book)
            new_picture.save()
            return HttpResponseRedirect('/web/plant_home')
        except Exception as e:
            print e
            return HttpResponseRedirect('/web/plant_home')
    return HttpResponseRedirect('/web/plant_home')


def picture_delete(request, id):
    try:
        picture = Picture.objects.get(id=id)
        picture.delete()
        return HttpResponseRedirect('/web/plant_home')
    except:
        pass
    return HttpResponseRedirect('/web/plant_home')


def plant_home(request):
    all_picture = Picture.objects.all()
    reply = {
        "all_picture":  all_picture,
        "username": request.user.username,
        'active_class': 4
    }
    return render(request, "newadmin/plantform_home.html", reply)


def send_message(request):
    return render(request, "newadmin/send_message.html")


def backmsg(request):
    if request.method=='POST':
        phone = request.POST['phone']
        name = request.POST['name']
        time = request.POST['time']
        send_borrow_message(phone,name,time)
        return render(request, "newadmin/send_message.html")
    return render(request, "newadmin/send_message.html")


def back_wechat(request):
    if request.method=='POST':
        openid = request.POST['openid']
        name = request.POST['name']
        time = request.POST['time']
        send_back_wechat(openid,name,time)
        return render(request, "newadmin/send_message.html")
    return render(request, "newadmin/send_message.html")


def feedback(request):
    """
    反馈
    :param request:
    :return:
    """
    if request.method == 'POST':
        id = request.POST['id']
        back_content = request.POST['back_content']
        try:
            feed_back = FeedBack.objects.get(id=id)
            feed_back.back_state = True
            feed_back.back_content = back_content
            feed_back.save()
        except:
            return render(request,"")
    return




