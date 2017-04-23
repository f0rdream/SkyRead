from rest_framework.serializers import (
    SerializerMethodField,
    ModelSerializer,
    ValidationError,
    DateTimeField,
    )
from .models import BorrowItem
from accounts.models import WeChatUser
class BorrowItemCreateSerializer(ModelSerializer):
    class Meta:
        # borrow_time = DateTimeField(allow_null=False)
        # return_time = DateTimeField(allow_null=False)
        model=BorrowItem
        fields =[
            'isbn13',
            'borrow_time',
            'return_time',
            'library_name',
            'location',
        ]

    def validate(self, data):
        isbn13 = data.get('isbn13')
        borrow_time = data.get('borrow_time')
        return_time = data.get('return_time')
        library_name = data.get('library_name')
        location = data.get('location')

        if not isbn13:
            raise ValidationError('lack isbn13')
        if not borrow_time:
            raise ValidationError('lack borrow_time')
        if not return_time:
            raise ValidationError('lack return_time')
        if not library_name:
            raise ValidationError('lack library_name')
        if not location:
            raise ValidationError('lack location')
        return data
class BorrowItemDetailSerializer(ModelSerializer):
    user = SerializerMethodField()
    nickname = SerializerMethodField()
    borrow_time = SerializerMethodField()
    return_time = SerializerMethodField()
    class Meta:
        model = BorrowItem
        fields = [
            'id',
            'isbn13',
            'user',
            'borrow_time',
            'return_time',
            'library_name',
            'location',
            'nickname',
        ]
    def get_user(self,obj):
        return str(obj.user.username)
    def get_nickname(self,obj):
        username = obj.user.username
        try:
            wechatuser = WeChatUser.objects.get(openid=username)
            nickname = wechatuser.nickname
            return nickname
        except:
            return None
    def get_borrow_time(self,obj):
        return obj.borrow_time
    def get_return_time(self,obj):
        return obj.return_time



