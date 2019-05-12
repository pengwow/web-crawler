# # -*- coding: utf-8 -*-
# from bs4 import BeautifulSoup
# import requests
# import json
# from urllib.parse import quote
# SPLASH_URL = "http://192.168.99.100:8050/"
# html = '''
# <div class="pt1"><!--B1--><span class="qseq">1．</span>（2019•深圳二模）函数<span dealflag="1" class="MathJye" mathtag="math" style="whiteSpace:nowrap;wordSpacing:normal;wordWrap:normal"><font class="MathJye_mi">f</font>(<font class="MathJye_mi">x</font>)＝<table cellpadding="-1" cellspacing="-1" style="margin-right:1px"><tbody><tr><td style="border-bottom:1px solid black;padding-bottom:1px;font-size:90%"><table cellspacing="-1" cellpadding="-1"><tbody><tr><td style="font-size: 14px; vertical-align: top; position: relative;"><div hassize="7" class="sqrt" style="transform: scale(1, 1.17647);">⎷</div></td><td style="padding:0;padding-left: 2px; border-top: black 1px solid;line-height:normal;padding-top:1px">1−<span><span><font class="MathJye_mi">x</font></span><span style="vertical-align:super;font-size:90%">2</span></span></td></tr></tbody></table></td></tr><tr><td style="padding-top:1px;font-size:90%"><font class="MathJye_mi">l</font><font class="MathJye_mi">g</font>|<font class="MathJye_mi">x</font>|</td></tr></tbody></table></span>的图象大致为（　　）<!--E1--></div>
# '''
#
# # while True:
# #     headers = {
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
# #     }
# #
# #
# #     response = requests.get(SPLASH_URL + 'render.html?'+url)
# #
# #     print(response.text)
#
# point_soup = BeautifulSoup(html, 'html')
# aaa = point_soup.get_text()
# print(aaa)
#     # table.append(item.text)
#     # if not title:
#     #     continue
#     # print(title.text)
#     # content_html = download_soup.find('div',class_='JYE_TAB_SUB JYE_TAB_SUB_2')
#     # print(content_html.text)
#     #
#     # # table = list()
#     # # content_class = 'JYE_TAB_SUB JYE_TAB_SUB_{index}'
#     # #
#     # #
#     # # #content = download_soup.select_one('div', class_='JYE_TAB_SUB')
#     # # try:
#     # #     for item in range(len(li)):
#     # #         table_name = li[item].text
#     # #         content = download_soup.select_one('div.JYE_TAB_SUB.JYE_TAB_SUB_' + str(item * 2))
#     # #         if content:
#     # #             content = content.text
#     # #             print(table_name,content)
#     # #     # table.append(item.text)
#     # # except Exception as e:
#     # #     print(e)
#     # break
#     #
#     #
#     #
#
#
#


test_str = '''
次根式的运算结果要化为二次根．<br/><div class="point-card"><h1><b>二次根式的运算</b></h1><div class="point-card-body"  ondbclick='fixbox()'><div>二次根的混合运算是二根式乘、除法及加减法运算的综用．学习次根式的混合运算应注意下几：<br/>在运算中每个根式可以做是一个“单项式“多个同类二次式的和看“多项式“．<br/>在根式的运算中，如能结合目特，灵活用二根式的性质，选择恰当的解题途径，往往事半倍．</div></div></div>
'''
import random
aa = random.random()
print(aa)
from bs4 import BeautifulSoup

download_soup = BeautifulSoup(test_str, 'lxml')
title = download_soup.find('div')
print(title.text)

import datetime
print(datetime.datetime.now().strftime('%Y-%m-%d'))