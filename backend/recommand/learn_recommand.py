# coding:utf-8
# 推荐系统实践书本源码
# train ={'user':'item','user1':'item1'}
# # for user in train.items():
# #     print user
import random

import math


def SplitData(data,M,k,seed):
    """
    数据分集,个数有问题
    :param data: 原始数据
    :param M: 份数
    :param k:
    :param seed: 固定的随机种子
    :return: train,test数据集合
    """
    test = []
    train = []
    random.seed(seed)
    for user,item in data:
        if random.randint(0,M) == k:
            test.append([user,item])
        else:
            train.append([user,item])
    return train,test

def Recall(train,test,N):
    """
    召回率,即推荐列表的击中数目
    :param train:
    :param test:
    :param N:向用户推荐的数目
    :return:
    """
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        # GetRecommendation(user,N)是得到对这个用户N个推荐
        rank = GetRecommendation(user,N)
        for item,pui in rank:
            if item in tu:
                hit += 1
        all += len(tu)
    return hit /(all*1.0)

def Precision(train,test,N):
    """
    计算准确率,即推荐的击中数处以总数
    :param train:
    :param test:
    :param N:
    :return:
    """
    hit = 0
    all = 0
    for user in train.keys():
        tu = test[user]
        rank = GetRecommendation(user,N)
        for item,pui in rank:
            if item in tu:
                hit += 1
        all += N
    return hit /(all*1.0)

def Coverage(train,test,N):
    """
    得到覆盖率
    """
    recommend_items = set()
    all_items = set()
    for user in train.keys():
        for item in train[user].keys():
            all_items.add(item)
        rank = GetRecommendation(user,N)
        for item,pui in rank:
            recommend_items.add(item)
    return len(recommend_items) / (len(all_items) * 1.0)
def Popularity(train,test,N):
    pass
# 余弦相似度 = (交集) / sqrt(len(a) * len(b))

def UserSimilarity(train):
    # 建立 物品-用户倒排表
    item_users = dict()
    for u,items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)
    # 计算余弦相似度
    C = dict()
    N = dict()
    for i,users in item_users.items():
        for u in users:
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                C[u][v] += 1
    W = dict()
    for u,related_users in C.items():
        for v,cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W

# item_users = {'a':{'A','B'},'b':{'B','C'},'c':{'A','B','C'}}
# C = dict()
# N = dict()
# for i, users in item_users.items():
#     for u in users:
#         N[u] += 1
#         for v in users:
#             if u == v:
#                 continue
#             C[u][v] += 1
# W = dict()
# for u, related_users in C.items():
#     for v, cuv in related_users.items():
#         W[u][v] = cuv / math.sqrt(N[u] * N[v])
# print W
