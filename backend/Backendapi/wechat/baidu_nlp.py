#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-9-4 下午11:46
@Author  : TangZongYu
@Desc    : 
"""
import jieba.posseg as pseg
words = pseg.cut("想学习机器学习")
for word in words:
    print word,word.flag