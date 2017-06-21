from django.contrib.auth.models import User
from rest_framework.fields import CharField, BooleanField
from rest_framework.serializers import ModelSerializer


class UserLoginSerializer(ModelSerializer):
    username = CharField()
    password = CharField(style={'input_type': 'password'})
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }