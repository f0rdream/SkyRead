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
for row in rs:
    amazon.spider(str(row[0]),row[1])
    count+=1
    print str(count) + "====================="
    time.sleep(1)
