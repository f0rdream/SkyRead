# coding:utf-8
# 从数据库中拿到title 和 isbn13
import time

from amazon_spider import AmazonSpider
import MySQLdb
conn = MySQLdb.Connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'd1',
    charset = 'utf8'
)
cursor = conn.cursor()
sql = "select title,isbn13 from " \
      "douban_p111 where average != ''"
cursor.execute(sql) #执行
print cursor.rowcount
rs = cursor.fetchall()
amazon = AmazonSpider()
count = 0
print len(rs)
for row in rs:
    amazon.spider(str(row[0]),row[1])
    count+=1
    print str(count) + "====================="
    time.sleep(1.5)

# 异常处理有问题,爬到9787111115205success
# 228====================
"""
买的电子版，部分描述为第四版内容，还有错题，漏部分题情况，总体一般
9787111115205success
228=====================
can't find this book
9787111115274success
229=====================
can't find this book
9787111115632success
"""
