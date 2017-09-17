#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 17-9-4 下午11:54
@Author  : TangZongYu
@Desc    :
"""
# string = "<!--
# var x='/decrypredir.aspx?d=';
# pjac0='';
# pjac0+= 'http://p.yiqifa';
# pjac0+= unescape('%u002E%u0063%u006F%u006D%u002F%u006E%u003F%u006B%u003D%u0032%u006D%u004C%u0045%u0072%u006E');
# pjac0+= 'KL6cLErI6H2mLEr';
# pjac0+= 'nzSWQL7WEDs6n4H';
# pjac0+= '6ntL6Zqf1JFmPcy';
# pjac0+= 'HkQLErJBw153F1J';
# pjac0+= '3srIW-&t=http:/';
# pjac0+= '/product.china-';
# pjac0+= unescape('%u0070%u0075%u0062%u002E%u0063%u006F%u006D%u002F%u0034%u0039%u0036%u0030%u0034%u0038%u0030');
# pjac1='';
# pjac1+= 'http://product.';
# pjac1+= unescape('%u0064%u0061%u006E%u0067%u0064%u0061%u006E%u0067%u002E%u0063%u006F%u006D%u002F%u0032%u0033');
# pjac1+= unescape('%u0039%u0037%u0035%u0031%u0036%u0%u002E%u0063%u006F%u006D%u002F%u006E%u003F%u006B%u003D%u0032%u006D%u004C%u0045%u0072%u006E033%u002E%u0068%u0074%u006D%u006C');
# pjac2='';
# pjac2+= 'http://p.yiqifa';
# pjac2+= unescape('%u002E%u0063%u006F%u006D%u002F%u006E%u003F%u006B%u003D%u0031%u0035%u0034%u0065%u0043%u004A');
# pjac2+= 'DmrI6H6n3l6cLEr';
# pjac2+= 'I6H2mLErnDS6nMH';
# pjac2+= '6n276NDSrn2F6lD';book.beifa';book.beifbook.beifa';book.beifa';book.beifa';a';
# pjac2+= 'FrI6HkQLErn3mWE';
# pjac2+= 'yw6Ny9rIW-&t=ht';# pjac2+= '6n276NDSrn2F6lD';book.beifa';book.beifbook.beifa';book.beifa';book.beifa';a';

# pjac2+= 'tp://book.beifa';
# pjac2+= 'book.com/produc';
# pjac2+= 't/BookDetail.as';
# pjac2+= 'px?Plucode=7111';
# pjac2+= unescape('%u0035%u0033%u0037%u0034%u0030%u0026');
# pjac3='';
# pjac3+= 'http://www.jarh';
# pjac3+= unescape('%u0075%u002E%u0063%u006F%u006D%u002F%u0062%u006F%u006F%u006B%u002D%u0031%u0033%u0039%u0031');
# pjac3+= '337.html?u=j207';
# pjac3+= unescape('%u0035');
# pjac4='';
# pjac4+= 'http://c.duomai';
# pjac4+= unescape('%u002E%u0063%u006F%u006D%u002F%u0074%u0072%u0061%u0063%u006B%u002E%u0070%u0068%u0070%u003F');
# pjac4+= 'site_id=133074&';
# pjac4+= 'aid=182&euid=&t';
# pjac4+= '=http://detail.';
# pjac4+= 'bookuu.com/3546';
# pjac4+= unescape('%u0039%u0030%u0039%u002E%u0068%u0074%u006D%u006C');
# pjac5='';
# pjac5+= 'http://p.yiqifa';
# pjac5+= unescape('%u002E%u0063%u006F%u006D%u002F%u006E%u003F%u006B%u003D%u0032%u006D%u004C%u0045%u0072%u006E');
# pjac5+= 'tF1ZLErI6H2mLEr';
# pjac5+= 'n2e1QL7WEDs6n4H';
# pjac5+= '6l27rI6HkQLErnX';
# pjac5+= 'yWEDe3EzLrnXQMJ';
# pjac5+= 'WmRZL-&t=http:/';
# pjac5+= '/item.winxuan.c';
# pjac5+= unescape('%u006F%u006D%u002F%u0031%u0032%u0030%u0031%u0033%u0030%u0037%u0034%u0030%u0036');
# pjac6='';
# pjac6+= 'http://c.duomai';
# pjac6+= unescape('%u002E%u0063%u006F%u006D%u002F%u0074%u0072%u0061%u0063%u006B%u002E%u0070%u0068%u0070%u003F');
# pjac6+= 'site_id=133074&';
# pjac6+= 'aid=61&euid=&t=';
# pjac6+= 'http://item.jd.';
# pjac6+= 'com/11928293.ht';
# pjac6+= unescape('%u006D%u006C');
# pjac7='';
# pjac7+= 'http://www.wl.c';
# pjac7+= unescape('%u006E%u002F%u0038%u0037%u0031%u0031%u0032%u0035%u0034%u002F');
# //-->"

import HTMLParser
html_parser = HTMLParser.HTMLParser()
# print html_parser.unescape()
txt = "%u002E%u0063%u006F%u006D%u002F%u006E%u003F%u006B%u003D%u0032%u006D%u004C%u0045%u0072%u006E"

import cgi
html = cgi.escape(txt)
print html