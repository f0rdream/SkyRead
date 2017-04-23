from django.shortcuts import render
from serializers import UserProfileDetailSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .models import WeChatUser
# Create your views here.
class UserProfileDetailAPIView(ListAPIView):
    serializer_class = UserProfileDetailSerializer
    permission_classes = [IsAuthenticated]
    # lookup_field = 'user_stu_id'

    def get_queryset(self):
        queryset = WeChatUser.objects.filter(openid=self.request.user.username)
        return queryset