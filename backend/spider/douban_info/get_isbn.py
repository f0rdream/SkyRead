# coding:utf-8
# 获取书籍的isbn
ch_isbn = "9787"
stop_isbn = ""
def get_book_isbn(press_code,begin_number,end_number):
    """
    得到一本书籍的完整isbn,完全遍历
    :param press_code: 出版社编码
    :param begin_number:开始编号,为了限制一次爬取数目
    :param end_number:结束编号
    :return:book_isbn
    """
    isbn_dict = []
    global count
    count = 0
    book_isbn = ''
    if len(press_code) == 2:
        for i in range(begin_number,end_number):
            book_isbn = connect_code(press_code,i)
            isbn_dict.append(book_isbn)
    elif len(press_code) == 3:
        for i in range(begin_number,end_number):
            book_isbn = connect_code(press_code, i)
            isbn_dict.append(book_isbn)
    elif len(press_code) == 4:
        for i in range(begin_number,end_number):
            book_isbn = connect_code(press_code, i)
            isbn_dict.append(book_isbn)
    elif len(press_code) == 5:
        for i in range(begin_number,end_number):
            book_isbn = connect_code(press_code,i)
            isbn_dict.append(book_isbn)
    else:
        print "出版社编码错误"
        return None
    return isbn_dict


def connect_code(press_code,i):
    code_digit = 8-len(press_code)   # 未固定的位数
    prefix_code = ch_isbn+press_code #前缀
    check_code = "1"  # 校验
    str_i = str(i)
    book_code = str_i.zfill(code_digit)
    book_isbn = prefix_code + book_code + check_code
    global count
    count += 1
    return book_isbn