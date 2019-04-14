# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
from urllib.parse import quote
SPLASH_URL = "http://192.168.99.100:8050/"
url = 'http://www.jyeoo.com/math3/api/pointcard?a=15'

lua='''
function main(splash,args)
    splash:go("http://www.jyeoo.com/math3/api/pointcard?a=15")
    splash:wait(1)
    return {
        html=splash.html(),
    }
end
'''
url=SPLASH_URL +'execute?lua_source='+quote(lua)
response=requests.get(url)
print()
# while True:
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
#     }
#
#
#     response = requests.get(SPLASH_URL + 'render.html?'+url)
#
#     print(response.text)
html = json.loads(response.text).get('html')
point_soup = BeautifulSoup((html.replace('<br>','\n')).replace('<br/>',''), 'lxml')
title = point_soup.find('b')
li = point_soup.find_all('li')
print(title.text)
for item in range(len(li)):
    table_name = li[item].text
    content = point_soup.select_one('div.JYE_TAB_SUB.JYE_TAB_SUB_' + str(item * 2))
    if content:
        content = content.text
        print(table_name,'\n',content)
    # table.append(item.text)
    # if not title:
    #     continue
    # print(title.text)
    # content_html = download_soup.find('div',class_='JYE_TAB_SUB JYE_TAB_SUB_2')
    # print(content_html.text)
    #
    # # table = list()
    # # content_class = 'JYE_TAB_SUB JYE_TAB_SUB_{index}'
    # #
    # #
    # # #content = download_soup.select_one('div', class_='JYE_TAB_SUB')
    # # try:
    # #     for item in range(len(li)):
    # #         table_name = li[item].text
    # #         content = download_soup.select_one('div.JYE_TAB_SUB.JYE_TAB_SUB_' + str(item * 2))
    # #         if content:
    # #             content = content.text
    # #             print(table_name,content)
    # #     # table.append(item.text)
    # # except Exception as e:
    # #     print(e)
    # break
    #
    #
    #



