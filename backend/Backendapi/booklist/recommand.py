# coding:utf-8
# 推荐算法脚本,包括基于用户的协同过滤
import math
import operator
import time

import MySQLdb
begin = time.time()


def get_default_train_dict():
    """
    得到用于训练的user-item模型
    :return:
    """
    train_dict = dict()
    conn = MySQLdb.Connect(
            host = '127.0.0.1',
            port = 3306,
            user = 'root',
            passwd = '123456',
            db = 'douban_user',
            charset = 'utf8'
        )
    cursor = conn.cursor()
    sql = "select distinct * from user_item"
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
    new_conn = MySQLdb.Connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123456',
        db='douban_user',
        charset='utf8'
    )
    C =dict()
    for i in sys_user_items:
        sql1 = "select users from item_users where item='%s'" % i
        new_cursor = new_conn.cursor()
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
def get_related_user():
    related_users = single_user_similarity(get_default_train_dict(),'TANG',['1885170','10769749','3296317',
                                                        '10517238','1286547','1082154',
                                                        '5336893','25779298','2130743'])
    print related_users


def SingleRecommend(user,single_related_users,K,train_dict):
    # 先选出与user 相似度最高的K个用户
    # 先提取出没有发生过行为的物品
    # 然后计算 WaB+WaC 为对物品的兴趣度
    # 取两个用户

    rank = dict()
    new_list = sorted(single_related_users.items(),key=operator.itemgetter(1),reverse=True)
    K_list = new_list[0:K]
    for v,wuv in K_list:
        for i in train_dict[v]:
            if i in train_dict[user]:
                continue
            if not rank.has_key(i):
                rank[i] = 0.0
            rank[i] += wuv
    return rank

train_dict['TANG'] = ['1885170','10769749','3296317',
                        '10517238','1286547','1082154',
                        '5336893','25779298','2130743']
rank =  SingleRecommend('TANG',related_users,30,train_dict)
new_list = sorted(rank.items(),key=operator.itemgetter(1),reverse=True)
print "get the recommand--------"

for i in new_list[25:50]:
    print i
print "------"+str(time.time()-begin)+"-------"