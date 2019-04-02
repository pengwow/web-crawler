# -*- coding:utf-8 -*-
from jyeoo.items import LibraryChapterItem
from scrapy_splash import SplashRequest
import scrapy
import uuid
from scrapy.http.cookies import CookieJar
from jyeoo.common.utils import get_valid_cookie, get_chapter_url

LEVEL_SUBJECTS = "http://www.jyeoo.com/math3/ques/search?f=0"


class LibraryChapter(scrapy.Spider):
    name = "library_chapter"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie()
        chapter_url = get_chapter_url()
        if cookie:
            for url in chapter_url:
                yield SplashRequest(url=url, callback=self.parse, cookies=cookie)
        else:
            pass  # TODO:待添加cookie处理

    def parse(self, response):
        sub_obj = response.xpath('//ul[@id="JYE_POINT_TREE_HOLDER"]//li')
        for item in sub_obj:
            lc_item = LibraryChapterItem()
            lc_item['id'] = str(uuid.uuid1())
            pk = item.xpath('./@pk').get()
            lc_item['pk'] = pk
            temp_list = pk.split('~')

            lc_item['name'] = item.xpath('./@nm').get()

            if temp_list[-1]:
                lc_item['library_id'] = temp_list[-1]
                parent_id = temp_list[temp_list.index(temp_list[-1]) - 1]
                lc_item['parent_id'] = ''
                if parent_id != lc_item['library_id']:
                    lc_item['parent_id'] = parent_id
            else:
                lc_item['library_id'] = temp_list[-2]
                parent_id = temp_list[temp_list.index(temp_list[-2]) - 1]
                lc_item['parent_id'] = ''
                if parent_id != lc_item['library_id']:
                    lc_item['parent_id'] = parent_id
            yield lc_item
