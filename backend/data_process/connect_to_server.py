# coding:utf-8
# 连接到远程数据库
import MySQLdb
conn = MySQLdb.Connect(
    host = '120.24.210.212',
    port = 3306,
    user = 'root',
    passwd = '1234',
    db = 'softcup',
    charset = 'utf8'
)

cursor = conn.cursor()
sql = 'insert into test values("yu",123)'
cursor.execute(sql)
conn.commit()
conn.close()