# coding:utf-8
# 推荐算法脚本,包括基于用户的协同过滤
import math
import operator
import time
from django.core.cache import cache
import MySQLdb
begin = time.time()
from django.db import connection

def get_default_train_dict():
    """
    得到用于训练的user-item模型
    :return:
    """
    train_dict = dict()
    cursor = connection.cursor()
    sql = "select distinct * from user_record.user_item"
    cursor.execute(sql)
    rs = cursor.fetchall()
    for row in rs:
        user = row[0]
        items_in_string = row[1]
        items_list = items_in_string.split("&")
        items_list.remove("")
        if not train_dict.has_key(user):
            train_dict[user] = items_list
        else:
            continue
    return train_dict


def single_user_similarity(train_dict,sys_user,sys_user_items):
    # 建立物品-用户倒排表

    C =dict()
    for i in sys_user_items:
        sql1 = "select users from user_record.item_users where item='%s'" % i
        new_cursor = connection.cursor()
        new_cursor.execute(sql1)
        new_rs  = new_cursor.fetchall()
        users = list()
        for i in new_rs:
            users.append(i[0])
        for v in users:
            if v == sys_user:
                continue
            if not C.has_key(v):
                C[v] = 0.0
            C[v] += 1/math.log(1+len(users))
            # 计算最后的相似度矩阵W
    print "calc the W"
    W = dict()
    for v, cuv in C.items():
        if not W.has_key(v):
            W[v] = 0.0
        W[v] = cuv / math.sqrt(len(sys_user_items) * len(train_dict[v]))
    return W


def single_user_recommend(user,single_related_users,K,add_sysuser_train_dict):
    # 先选出与user 相似度最高的K个用户
    # 先提取出没有发生过行为的物品
    # 然后计算 WaB+WaC 为对物品的兴趣度
    # 取两个用户
    rank = dict()
    new_list = sorted(single_related_users.items(),key=operator.itemgetter(1),reverse=True)
    K_list = new_list[0:K]
    for v,wuv in K_list:
        for i in add_sysuser_train_dict[v]:
            if i in add_sysuser_train_dict[user]:
                continue
            if not rank.has_key(i):
                rank[i] = 0.0
            rank[i] += wuv
    return rank

# rank =  SingleRecommend('TANG',related_users,30,train_dict)
# new_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)
# print "get the recommend--------"
#
# for i in new_list[25:50]:
#     print i
# print "------"+str(time.time()-begin)+"-------"


def book_recommend(username,douban_id_list):
    # 得到缓存
    train_dict_cache = cache.get("train_dict_cache")
    if train_dict_cache:
        print "print get train_dict_cache"
        default_train_dict = train_dict_cache
        related_user = single_user_similarity(default_train_dict,username,douban_id_list)
        default_train_dict[username] = douban_id_list
        rank = single_user_recommend(username,related_user,30,default_train_dict)
        new_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)
        for book in new_list:
            if book[0] in ['1770782', '1084336', '1008145', '1082154', '25862578',
                             '3259440', '1046265', '3211779', '2567698', '1017143',
                             '1007305', '1016300', '1040771', '20427187', '6082808',
                             '5275059', '1461903', '1200840', '1141406', '1041007',
                             '10554308', '3066477', '1068920', '4238362', '5363767',
                             '4242172', '1083428', '1090043', '1026425', '2256039',
                             '1873231', '1071241', '3995526', '1400705', '1039487',
                             '1041482', '1059406', '1023045', '2209098', '4742918',
                             '1022060', '4886245', '3879301', '1529893', '1009257',
                             '1057244', '1858513', '1066462', '4913064', '1082334',
                             '25747921', '2062200', '1255625', '3646172', '1049219',
                             '1975797', '4074636', '1432596', '2250587', '1045818',
                             '1029791', '1049189', '1948901', '1361264', '10594787',
                             '1013129', '2022979', '3426869', '1059419', '1050339',
                             '1085860', '1007914', '1019568', '26340138', '1089243',
                             '1065970', '3598313', '4714734', '1827374', '2159042',
                             '1029159', '6388661', '1030052', '3369600', '1949338',
                             '5317075',]:
                new_list.remove(book)
        return new_list[:20]
    else:
        default_train_dict = get_default_train_dict()
        cache.set("train_dict_cache",default_train_dict,2592000)
        print "success get the train_dict"
        related_user = single_user_similarity(default_train_dict,username,douban_id_list)
        default_train_dict[username] = douban_id_list
        rank = single_user_recommend(username,related_user,30,default_train_dict)
        new_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)
        for book in new_list:
            if book[0] in ['1770782', '1084336', '1008145', '1082154', '25862578',
                             '3259440', '1046265', '3211779', '2567698', '1017143',
                             '1007305', '1016300', '1040771', '20427187', '6082808',
                             '5275059', '1461903', '1200840', '1141406', '1041007',
                             '10554308', '3066477', '1068920', '4238362', '5363767',
                             '4242172', '1083428', '1090043', '1026425', '2256039',
                             '1873231', '1071241', '3995526', '1400705', '1039487',
                             '1041482', '1059406', '1023045', '2209098', '4742918',
                             '1022060', '4886245', '3879301', '1529893', '1009257',
                             '1057244', '1858513', '1066462', '4913064', '1082334',
                             '25747921', '2062200', '1255625', '3646172', '1049219',
                             '1975797', '4074636', '1432596', '2250587', '1045818',
                             '1029791', '1049189', '1948901', '1361264', '10594787',
                             '1013129', '2022979', '3426869', '1059419', '1050339',
                             '1085860', '1007914', '1019568', '26340138', '1089243',
                             '1065970', '3598313', '4714734', '1827374', '2159042',
                             '1029159', '6388661', '1030052', '3369600', '1949338',
                             '5317075',]:
                new_list.remove(book)
        return new_list[:20]


def user_recommend(username,douban_id_list):
    train_dict_cache = cache.get("train_dict_cache")
    if train_dict_cache:
        default_train_dict = train_dict_cache
        user_list=single_user_similarity(default_train_dict,username,douban_id_list)
        new_list = sorted(user_list.items(), key=operator.itemgetter(1), reverse=True)
        K_list = new_list[0:9]
        print "here"
        print K_list
        return  K_list
    else:
        default_train_dict = get_default_train_dict()
        user_list = single_user_similarity(default_train_dict, username, douban_id_list)
        new_list = sorted(user_list.items(), key=operator.itemgetter(1), reverse=True)
        K_list = new_list[0:9]
        print K_list
        print "here"
        return K_list