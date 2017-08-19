import MySQLdb
conn = MySQLdb.Connect(
    host = 'tdsql-axy3u6tl.sh.cdb.myqcloud.com',
    port = 92,
    user = 'wangyang',
    passwd = 'skyread@614',
    db = 'skyread',
    charset = 'utf8'
)
cursor = conn.cursor()


def get_author_index(author):
    author_for_index = ''
    for i in author:
        if i == "'" or i == "" or i == '\\':
            continue
        search_sql = "select number from bookinfo.char_number where title='%s'" % i
        cursor.execute(search_sql)
        search_rs = cursor.fetchall()
        if search_rs:
            author_for_index += '#'
            author_for_index += str(search_rs[0][0])
        else:
            print "get something new============================="
            number = str(50000).zfill(8)
            insert_sql = "insert into bookinfo.char_number values ('%s','%s')" % (i, number)
            cursor.execute(insert_sql)
            conn.commit()
            author_for_index += '#'
            author_for_index += number
    return author_for_index


def get_title_index(title):
    author_for_index = ''
    for i in title:
        if i == "'" or i == "" or i == '\\':
            continue
        search_sql = "select number from bookinfo.char_number where title='%s'" % i
        cursor.execute(search_sql)
        search_rs = cursor.fetchall()
        if search_rs:
            author_for_index += '#'
            author_for_index += str(search_rs[0][0])
        else:
            print "get something new============================="
            number = str(50000).zfill(8)
            insert_sql = "insert into bookinfo.char_number values ('%s','%s')" % (i, number)
            cursor.execute(insert_sql)
            conn.commit()
            author_for_index += '#'
            author_for_index += number
    return author_for_index

