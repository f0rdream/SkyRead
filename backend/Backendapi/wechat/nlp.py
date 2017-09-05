#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-9-5 下午11:42
@Author  : TangZongYu
@Desc    : 
"""

def get_seach(content):
    import jieba.posseg as pseg
    words = pseg.cut(content)
    for word in words:
        print word.flag

get_seach("学习机器学习")
