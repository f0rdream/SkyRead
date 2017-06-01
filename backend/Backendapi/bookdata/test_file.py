#coding: utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
author = '&约翰 A·卡斯林&菲利普·科特勒&'
author2 = '&'
author3 = '&罗培羽'
author4 = '&罗培羽&约翰 A·卡斯林&&菲利普·科特勒&'
author5 = ''

test_author = ''

# if test_author == '':
#     author = None
# elif test_author == '&':
#     author = None
# elif
def get_author(authors):
    if authors == '' or authors == '&':
        return None
    else:
        author_list = []
        authors = authors.split('&')
        for author in authors:
            if author == '':
                continue
            else:
                author_list.append(author)
        return author_list

tags = '&供应链&企业管理&管理&马士华'
def get_tags(tags):
    if tags == '':
        return None
    else:
        taglist = []
        tags = tags.split('&')
        for tag in tags:
            if tag == '':
                continue
            else:
                taglist.append(tag)
        return taglist


refer_id = "&1461903&1016300&1040771&1856285&1084336&1141406&1008145&25862578&2256039&3259440"
refer_list = list()
refer = refer_id.split("&")
for i in range(1,len(refer)):
    print refer[i]
    refer_list.append(refer[i])

