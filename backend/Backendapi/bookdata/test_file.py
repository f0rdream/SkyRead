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