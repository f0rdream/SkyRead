#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-9-4 下午11:46
@Author  : TangZongYu
@Desc    : 
"""
from aip import AipNlp
# 定义常量
APP_ID = '10091919'
API_KEY = 'S4SVTBvaB4zIWaAnU9W2u9CQ'
SECRET_KEY = 'bFFrfPgq69Hv6fyD75bvFBAr0RODMkdM'

# 初始化AipNlp对象
aipNlp = AipNlp(APP_ID, API_KEY, SECRET_KEY)
result = aipNlp.wordpos("想学习机器学习")

print result