# coding:utf-8
from serializers import (UserProfileDetailSerializer,
                         SendMessageSerializer,
                         CheckAPISerializer,
                         PhoneUserCreateSerializer,
                         FeedBackSerializer,
                         FeedBackDetailSerializer,
                         ChangeTimesSerializer,
                         AddLabelSerializer,
                         LabelSerializer,
                         BookListCreateSerializer,
                         BookListIdSerializer,
                         CycleCommnetSerializer,
                         ListCommentDetailSerializer,
                         NoteCommentDetailSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from .models import (WeChatUser, PhoneUser, FeedBack,
                     StarList, UserCreateBookList, BookInList,
                     StarBookList, BookListComment)
from accounts_lib.phone_verify import send_message,verify
from l_lib.function import get_reply
from library.permissions import have_phone_register
from bookdata.models import Book, Note,NoteComment
from bookdata.serializers import ShortInto


class UserProfileDetailAPIView(APIView):
    """
    用户基本信息API
    """
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'user_stu_id'

    def get(self,request):
        openid = request.user.username
        w = WeChatUser.objects.get(openid=openid)
        serializer = self.serializer_class(w,data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class CheckAPIView(APIView):
    """
    手机,邮箱查重 API
    """
    serializer_class = CheckAPISerializer

    @staticmethod
    def check_info(phone_number=None,email=None):
        reply = {}
        if phone_number:
            phone_existed =  PhoneUser.objects.filter(phone_number=phone_number)
            if not phone_existed:
                reply['phone_existed'] = False
            else:
                reply['phone_existed'] = True
        if email:
            email_existed = PhoneUser.objects.filter(email=email)
            if not email_existed:
                reply['email_existed'] = False
            else:
                reply['email_existed'] = True
        return reply

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        email = serializer.validated_data['email']
        reply = self.check_info(phone_number,email)
        return Response(reply,HTTP_200_OK)


class SendMessageAPIView(APIView):
    """
    发送手机验证码
    """
    serializer_class = SendMessageSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        reply = send_message(phone_number)  # 发送验证码
        return Response(reply,HTTP_200_OK)


class PhoneUserCreateAPIView(APIView):
    """
    手机绑定
    """
    serializer_class = PhoneUserCreateSerializer

    def post(self,request):
        reply = {}
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']
        captcha = serializer.validated_data['captcha']
        # 先检验验证码
        if not verify(phone_number,captcha):
            reply['error_code'] = 1
            reply['data'] = {
                "phone_number":phone_number,
            }
            return Response(reply,HTTP_400_BAD_REQUEST)
        else:
            try:
                p = PhoneUser.objects.create(user=request.user,phone_number=phone_number)
                p.save()
                reply['data'] = {
                    "phone_number": phone_number,
                }
                return Response(reply,HTTP_201_CREATED)
            except:
                reply['error_code'] = 2
                return Response(reply,HTTP_400_BAD_REQUEST)


def open_order_message(request):
    """
    订阅消息的设置
    :param request:
    :return:
    """
    state = request.GET.get("state")
    user = request.user


class OrderMessageOpenOrClose(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        state = request.GET.get("state")
        if state == 'close':
            user = request.user
            phone_user = PhoneUser.objects.get(user=user)
            phone_user.order_message = False
            phone_user.save()
            return Response(get_reply(0, 'success'))
        elif state == 'open':
            user = request.user
            phone_user = PhoneUser.objects.get(user=user)
            phone_user.order_message = True
            phone_user.save()
            return Response(get_reply(0, 'success'))
        else:
            return Response(get_reply(113, 'fail'),HTTP_400_BAD_REQUEST)


class ReturnMessageOpenOrClose(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        state = request.GET.get("state")
        if state == 'close':
            user = request.user
            phone_user = PhoneUser.objects.get(user=user)
            phone_user.return_message = False
            phone_user.save()
            return Response(get_reply(0,'success'))
        elif state == 'open':
            user = request.user
            phone_user = PhoneUser.objects.get(user=user)
            phone_user.return_message = True
            phone_user.save()
            return Response(get_reply(0, 'success'),HTTP_200_OK)
        else:
            return Response(get_reply(113,'fail'),HTTP_400_BAD_REQUEST)


class ChangeTimeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangeTimesSerializer

    def post(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17, 'not register with phone')
            return Response(reply,HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        recommend_times = serializer.validated_data['recommend_times']
        try:
            phone_user = PhoneUser.objects.get(user=request.user)
            phone_user.recommend_times = recommend_times
            phone_user.save()
            return Response(get_reply(0,'success'),HTTP_200_OK)
        except:
            return Response(get_reply(150,'fail to change time'),HTTP_400_BAD_REQUEST)


class FeedBackView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedBackSerializer

    def post(self,request):
        if not have_phone_register(user=request.user):
            reply = get_reply(17, 'not register with phone')
            return Response(reply, HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        try:
            feedback = FeedBack.objects.create(user=request.user,
                                               content=content,
                                               back_content=u'暂无回复')
            feedback.save()
            return Response(HTTP_200_OK)
        except:
            reply = get_reply(151, 'post feedback fail')
            return Response(reply,HTTP_403_FORBIDDEN)

    def get(self,request):
        try:
            queryset = FeedBack.objects.filter(user=request.user)
            serializer = FeedBackDetailSerializer(queryset, data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except:
            return Response(HTTP_404_NOT_FOUND)


class AddLabelView(APIView):
    """
    收藏某个标签到首页
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddLabelSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        key_word = serializer.validated_data['label_name']
        try:
            star_list = StarList.objects.create(user=request.user,
                                                list_type=0,
                                                key_word=key_word)
            star_list.save()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_403_FORBIDDEN)

    def get(self,request):
        queryset = StarList.objects.filter(user=request.user,list_type=0)
        serializer = LabelSerializer(queryset, data=request.data,many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,HTTP_200_OK)


class DeleteLabelView(APIView):
    """
    删除标签
    """
    permission_classes = [IsAuthenticated]

    def delete(self,request,pk):
        try:
            star_list = StarList.objects.get(pk=pk)
            star_list.delete()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_403_FORBIDDEN)


class BookListView(APIView):
    """
    用户创建书单
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BookListCreateSerializer

    def post(self, request):
        serializer = BookListCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        title = serializer.validated_data['title']
        comment = serializer.validated_data['comment']
        isbn13_list = serializer.validated_data['isbn13_list']
        # 找到第一本书的图片:
        try:
            book = Book.objects.get(isbn13=isbn13_list[0])
            img_id = book.img_id
            if img_id == "update_image":
                img_id = "--"
        except:
            img_id = "--"
        # 创建书单项:
        user_list = UserCreateBookList.objects.create(user=request.user,
                                                      title=title,
                                                      comment=comment,
                                                      img_id=img_id)
        user_list.save()
        # 向书单项中添加书籍
        for isbn13 in isbn13_list:
            try:
                book = Book.objects.get(isbn13=isbn13)
                book_in_list = BookInList.objects.create(book_list=user_list,
                                                         book=book)
                book_in_list.save()
            except Exception as e:
                print e
        return Response(HTTP_200_OK)

    def get(self, request):
        """获取自己建的书单"""
        queryset = UserCreateBookList.objects.filter(user=request.user)
        reply = list()
        for book_list in queryset:
            reply_dict = dict()
            reply_dict['id'] = book_list.id
            reply_dict['title'] = book_list.title
            reply_dict['comment'] = book_list.comment
            reply_dict['img_id'] = book_list.img_id
            reply.append(reply_dict)
        return Response(reply, HTTP_200_OK)


class StarBookListView(APIView):
    """收藏书单"""
    permission_classes = [IsAuthenticated]
    serializer_class = BookListIdSerializer

    def post(self,request):
        """收藏"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        list_id = serializer.validated_data['list_id']
        try:
            book_list = UserCreateBookList.objects.get(pk=list_id)
            star_book_list = StarBookList.objects.create(user=request.user,
                                                         book_list=book_list)
            star_book_list.save()
            book_list.star += 1
            book_list.save()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_404_NOT_FOUND)

    def get(self,request):
        queryset = StarBookList.objects.filter(user=request.user)
        reply = list()
        for i in queryset:
            reply_dict = dict()
            reply_dict['id'] = i.book_list.id
            reply_dict['title'] = i.book_list.title
            reply_dict['comment'] = i.book_list.comment
            reply_dict['img_id'] = i.book_list.img_id
            reply.append(reply_dict)
        return Response(reply, HTTP_200_OK)


class BookListDetailView(APIView):
    """
    书单详情和删除
    """
    def get(self,request,pk):
        try:
            book_list = UserCreateBookList.objects.get(pk=pk)
            reply_dict = dict()
            reply_dict['id'] = book_list.id
            reply_dict['title'] = book_list.title
            reply_dict['comment'] = book_list.comment
            reply_dict['img_id'] = book_list.img_id
            # 拿到用户名字
            star_count = StarBookList.objects.filter(book_list=book_list)
            reply_dict['star_count'] = book_list.star
            book_in_list = BookInList.objects.filter(book_list=book_list)
            books = list()  # 存储书单中所有的Book对象
            for i in book_in_list:
                books.append(i.book)
            serializer = ShortInto(books, data=[], many=True)
            serializer.is_valid(raise_exception=True)
            reply_dict['books_info'] = serializer.data
            return Response(reply_dict, HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)


class CycleView(APIView):
    """
    圈子内容
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, page):
        page = int(page)
        order = request.GET.get("order")
        if order == "star":
            # 按照热度排序
            # 先查书单15:
            list_queryset = UserCreateBookList.objects.order_by("star")[page*15-15:page*15]
            # 再查笔记5
            note_queryset = Note.objects.filter(shared=True)[page*5-5:page*5]
            reply = list()
            for i in range(5):
                small_list_qs = list_queryset[i*3:i*3+3]
                small_note_qs = note_queryset[i:i+1]
                for sl in small_list_qs:
                    sl_dict = dict()
                    sl_dict['title'] = sl.title
                    sl_dict['comment'] = sl.comment
                    sl_dict['img_id'] = sl.img_id
                    sl_dict['type'] = u"book_list"
                    sl_dict['id'] =  sl.id
                    reply.append(sl_dict)
                for sn in small_note_qs:
                    sn_dict = dict()
                    sn_dict['title'] = sn.title
                    sn_dict['comment'] = sn.comment
                    sn_dict['img_id'] = sn.book_img_url
                    sn_dict['type'] = u"note"
                    sn_dict['id'] = sn.id
                    reply.append(sn_dict)
            return Response(reply, HTTP_200_OK)
        elif order == "time":
            # 按照时间排序
            # 先查书单15:
            list_queryset = UserCreateBookList.objects.all()[page * 15 - 15:page * 15]
            # 再查笔记5
            note_queryset = Note.objects.filter(shared=True)[page * 5 - 5:page * 5]
            reply = list()
            for i in range(5):
                small_list_qs = list_queryset[i * 3:i * 3 + 3]
                small_note_qs = note_queryset[i:i + 1]
                for sl in small_list_qs:
                    sl_dict = dict()
                    sl_dict['title'] = sl.title
                    sl_dict['comment'] = sl.comment
                    sl_dict['img_id'] = sl.img_id
                    sl_dict['type'] = u"book_list"
                    sl_dict['id'] = sl.id
                    reply.append(sl_dict)
                for sn in small_note_qs:
                    sn_dict = dict()
                    sn_dict['title'] = sn.title
                    sn_dict['comment'] = sn.comment
                    sn_dict['img_id'] = sn.book_img_url
                    sn_dict['type'] = u"note"
                    sn_dict['id'] = sn.id
                    reply.append(sn_dict)
            return Response(reply, HTTP_200_OK)
        else:
            return Response(HTTP_404_NOT_FOUND)


class CycleSearchView(APIView):
    """
    搜索
    """
    permission_classes = [IsAuthenticated]

    def get(self,request):
        keyword = request.GET.get("keyword")
        # 先去查找书单
        list_queryset = UserCreateBookList.objects.filter(title__contains=keyword)
        # 再去查找笔记
        note_queryset = Note.objects.filter(title__contains=keyword)
        reply = list()
        for sl in list_queryset:
            sl_dict = dict()
            sl_dict['title'] = sl.title
            sl_dict['comment'] = sl.comment
            sl_dict['img_id'] = sl.img_id
            sl_dict['type'] = u"book_list"
            sl_dict['id'] = sl.id
            reply.append(sl_dict)
        for sn in note_queryset:
            sn_dict = dict()
            sn_dict['title'] = sn.title
            sn_dict['comment'] = sn.comment
            sn_dict['img_id'] = sn.book_img_url
            sn_dict['type'] = u"note"
            sn_dict['id'] = sn.id
            reply.append(sn_dict)
        return Response(reply, HTTP_200_OK)


class CycleListCommentView(APIView):
    """
    添加书单评论和笔记评论
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CycleCommnetSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        try:
            book_list = UserCreateBookList.objects.get(pk=pk)
            comment_obj = BookListComment.objects.create(book_list=book_list,
                                                         user=request.user,
                                                         content=content)
            comment_obj.save()
            return Response(HTTP_200_OK)
        except:
            return Response(HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            book_list = UserCreateBookList.objects.get(pk=pk)
            comment_queryset = BookListComment.objects.filter(book_list=book_list)
            serializer = ListCommentDetailSerializer(comment_queryset,
                                                     data=request.data,
                                                     many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data,HTTP_200_OK)
        except:
            return Response(HTTP_404_NOT_FOUND)


class CycleNoteCommentView(APIView):
    """
        添加书单评论和笔记评论
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CycleCommnetSerializer

    def post(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        content = serializer.validated_data['content']
        try:
            note = Note.objects.get(pk=pk)
            comment_obj = NoteComment.objects.create(note=note,
                                                         user=request.user,
                                                         content=content)
            comment_obj.save()
            return Response(HTTP_200_OK)
        except Exception as e:
            print e
            return Response(HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        try:
            note = Note.objects.get(pk=pk)
            comment_queryset = NoteComment.objects.filter(note=note)
            serializer = NoteCommentDetailSerializer(comment_queryset,
                                                     data=request.data,
                                                     many=True)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, HTTP_200_OK)
        except Exception as e :
            print e
            return Response(HTTP_404_NOT_FOUND)














