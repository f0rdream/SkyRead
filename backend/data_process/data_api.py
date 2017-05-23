import MySQLdb

conn = MySQLdb.Connect(
    host = '127.0.0.1',
    port = 3306,
    user = 'root',
    passwd = '123456',
    db = 'softcup',
    charset = 'utf8'
)
cursor = conn.cursor()
sql = "select title from douban_press01 where isbn13='9787010009292'"
cursor.execute(sql)
catalog = cursor.fetchall()
conn.commit()
conn.close()
print catalog[0][0]
with open('title.txt','a') as t:
    t.write(catalog[0][0].encode('utf-8'))