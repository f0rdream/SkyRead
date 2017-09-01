# coding:utf-8
from serializers import (UserProfileDetailSerializer,
                         SendMessageSerializer,
                         CheckAPISerializer,
                         PhoneUserCreateSerializer,
                         FeedBackSerializer,
                         FeedBackDetailSerializer,
                         ChangeTimesSerializer,
                         AddLabelSerializer,LabelSerializer)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from rest_framework.response import Response
from .models import WeChatUser,PhoneUser, FeedBack, StarList
from accounts_lib.phone_verify import send_message,verify
from l_lib.function import get_reply
from library.permissions import have_phone_register


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


class CreateBookListView(APIView):
    """
    用户创建书单
    """
    permission_classes = [IsAuthenticated]

    def post(self,request):








