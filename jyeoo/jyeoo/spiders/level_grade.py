# -*- coding:utf-8 -*-
from jyeoo.items import LevelGradeItem
import scrapy
from jyeoo.common.utils import get_valid_cookie

LEVEL_GRADE = "http://www.jyeoo.com/math3/ques/search?f=0"


class LevelGrade(scrapy.Spider):
    name = "level_grade"

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie()

        if cookie:
            yield scrapy.Request(url=LEVEL_GRADE, callback=self.parse, cookies=cookie)
        else:
            pass  # TODO:待添加cookie处理

    def parse(self, response):
        sub_obj = response.xpath('//div[@class="divBook"]').get()

        for item in sub_obj:
            lg_item = LevelGrade()
            lg_item['level_name'] = item.xpath('./dt/text()').get()
            lg_item['level_code'] = response.url
            #lg_item['grade_name'] =
            #lg_item['grade_code']




            yield lg_item
