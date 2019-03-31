# -*- coding:utf-8 -*-
from jyeoo.items import LevelSubjectsItem
import scrapy
from scrapy.http.cookies import CookieJar
from jyeoo.common.utils import get_valid_cookie

LEVEL_SUBJECTS = "http://www.jyeoo.com/math3/ques/search?f=0"


class LevelSubjects(scrapy.Spider):
    name = "level_subjects"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie()

        if cookie:
            yield scrapy.Request(url=LEVEL_SUBJECTS, callback=self.parse, cookies=cookie)
        else:
            pass  # TODO:待添加cookie处理

    def parse(self, response):
        sub_obj = response.css('.tip-pop').xpath('./dl')
        for item in sub_obj:
            level_name = item.xpath('./dt/text()').get()
            for sub_a in item.xpath('.//a'):
                ls_item = LevelSubjectsItem()
                # 授课层级名称 小学
                ls_item['level_name'] = level_name
                # 科目名称
                ls_item['subject_name'] = sub_a.xpath('./text()').get()
                # 科目URL
                ls_item['search_url'] = sub_a.xpath('./@href').get()
                # 科目编码
                ls_item['subject_code'] = ls_item['search_url'][1:].split('/')[0]
                # 授课层级Code
                ls_item['level_code'] = ls_item['search_url'][1:].split('/')[0]
                yield ls_item
