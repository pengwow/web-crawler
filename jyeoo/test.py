# -*- coding: utf-8 -*-
import nltk
import json
import urllib.request
from lxml import etree
url = 'http://www.jyeoo.com/math3/api/pointcard?a=15'


point_html = etree.parse(url,etree.HTMLParser())

ul = point_html.xpath('//ul/li')
for item in ul:
    ccc = etree.tostring(item.xpath('./text()'))
    #aaa =
    print(ccc)
