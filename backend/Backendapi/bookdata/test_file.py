#coding: utf-8
import  time
# import datetime
#
# d = datetime.datetime.now()
# a = "b2b3b4b5"
# b =  a.split("b")
# b.remove('')
# print str(time.strftime('%Y-%m-%d',time.localtime(time.time())))
# print str(time.strftime('%Y-%m-%d',time.localtime(time.time()+2419200)))
# print time.time()
# a =None
# if not a:
#     print "----"
# else:
#     print "～～～～"
import datetime
return_time = "2017-06-17"
date_list = return_time.split("-")
year = int(date_list[0])
month = int(date_list[1])
day = int(date_list[2])
return_date = datetime.datetime(year,month,day)
print return_date.date()

