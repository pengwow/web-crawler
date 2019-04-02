# -*- coding:utf-8 -*-
from jyeoo.items import LevelGradeItem
import scrapy
from jyeoo.common.utils import get_valid_cookie
from scrapy_splash.request import SplashRequest, SplashFormRequest
LEVEL_GRADE = "http://www.jyeoo.com/math3/ques/search?f=0"
scroll_script = """
function main(splash)
    splash:set_viewport_size(1028, 10000)
    splash:go(splash.args.url)
    local scroll_to = splash:jsfunc("window.scrollTo")
    scroll_to(0, 2000)
    splash:wait(15)
    return {
        html = splash:html()
    }
end
"""

class LevelGrade(scrapy.Spider):
    name = "level_grade"

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie()

        if cookie:
            # 需要动态js爬取
            yield SplashRequest(url=LEVEL_GRADE, callback=self.parse, cookies=cookie)
        else:
            pass  # TODO:待添加cookie处理

    def parse(self, response):
        aaa = response.xpath('//a[@class="next"]').get()

        print(aaa)
        sub_obj = response.xpath('//ul[@id="JYE_BOOK_TREE_HOLDER"]//li')
        for item in sub_obj:
            print(item.get())
            lg_item = LevelGradeItem()
            style_name = item.xpath('./@nm').get()
            style_idx = item.xpath('./@ek').get()
            level_li = item.xpath('./ul//li')
            for li_item in level_li:
                lg_item['id'] = li_item.xpath('./@bk')

                lg_item['grade_code'] = li_item.xpath('./@gd')
                lg_item['grade_name'] = li_item.xpath('./@nm')
            lg_item['level_name'] = ""
            lg_item['level_code'] = item.xpath('./@data-id').get()
            lg_item['grade_name'] = item.xpath('./text()').get()
             #= item.xpath('./@data-gd').get()
            yield lg_item
