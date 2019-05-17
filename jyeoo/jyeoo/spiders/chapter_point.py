# -*- coding:utf-8 -*-
from jyeoo.items import ChapterPointItem
import scrapy
from scrapy.http.cookies import CookieJar
from jyeoo.common.utils import get_valid_cookie, get_chapter_point_url, cookie_str_to_dict
from jyeoo.common.constant import STR

LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"
LOGIN_POST_URL = 'http://api.jyeoo.com/home/login?ReturnUrl=%2F'
JYEOO_INDEX = "http://www.jyeoo.com"


class ChapterPoint(scrapy.Spider):
    name = "chapter_point"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()

    # 是否登陆
    is_login = False

    cookie = None
    # db_session = DBSession()
    start_urls = dict()

    error_page_list = list()  # TODO: 待完成错误页的处理

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie(STR)
        self.start_urls = get_chapter_point_url()
        if not cookie:
            self.log("未获取到cookie!,需要登陆获取cookie")
        else:
            self.log("使用缓存的cookie,进行爬取知识点表")
            cookie_dict = cookie_str_to_dict(cookie)
            for start_urls in self.start_urls:
                url = start_urls['url']
                self.log("爬虫开始爬取 url:" + url)
                yield scrapy.Request(url=url, meta={'cookiejar': True,
                                                    'id': start_urls['id']
                                                    },
                                     cookies=cookie_dict,
                                     callback=self.parse)

    def parse(self, response):
        # 开始爬取
        point_id = response.meta.get('id')

        context = response.xpath('.//div[@class="point-card-body"]').get()

        chapter_point_item = ChapterPointItem()
        chapter_point_item['id'] = point_id
        chapter_point_item['content'] = context
        return chapter_point_item
