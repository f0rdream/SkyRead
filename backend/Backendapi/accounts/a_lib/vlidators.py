# coding:utf-8
import re
import re
from django.core.exceptions import ValidationError
class CheckString(object):
    """
    验证仅允许包含汉字、数字、字母、下划线、短横线、加号和问号
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        if not re.search(u'^[_a-zA-Z0-9\u4e00-\u9fa5\-\+\?]+$', value):
            raise ValidationError(u'%s contains illegal characters', value)
class PhoneValid(object):
    """
    手机号的合法性验证
    """
    def __init__(self, name):
        self.name = name

    def __call__(self, value, *args, **kwargs):
        prefix = ['13', '14', '15', '17', '18']
        if len(value) != 11:
            raise ValidationError('Please ensure the length is 11')
        if value[:2] not in prefix:
            raise ValidationError('Please ensure your phone number begin with 13,14,15,17,18')