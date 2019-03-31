# -*- coding:utf-8 -*-
from jyeoo.items import JyeooItem
import scrapy
from scrapy import FormRequest, Request
from jyeoo.settings import JYEEO_USER, JYEOO_PASSWORD
from scrapy.http.cookies import CookieJar
from jyeoo.common.constant import start_urls
from jyeoo.common.utils import get_valid_cookie
from jyeoo.model import DBSession, CookieInfo
import datetime

LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/math3/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"

JYEOO_INDEX = "http://www.jyeoo.com/"


class ItemBank(scrapy.Spider):
    name = "item_bank"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()

    # 是否登陆
    is_login = False

    cookie = None
    db_session = DBSession()

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie()

        if not cookie:
            self.log("未获取到cookie!,开始登陆获取cookie")
            yield scrapy.Request(url=LOGIN_URL, cookies=cookie, meta={'cookiejar': True}, callback=self.login_parse)
        else:
            self.log("使用缓存的cookie,进行爬取")
            for item in start_urls:
                self.log("爬虫开始爬取 url:" + item)
                yield scrapy.Request(url=item, cookies=cookie, meta={'cookiejar': True}, callback=self.parse)

    def login_parse(self, response):
        _login_dict = dict()
        _login_dict['Sn'] = ''
        # email = response.css('#Email::attr(value)').extract()
        # password = response.css('#Password::attr(value)').extract()
        userid = response.css('#UserID::attr(value)').extract()

        _login_dict['Email'] = JYEEO_USER

        _login_dict['Password'] = JYEOO_PASSWORD
        if len(userid) > 0:
            _login_dict['UserID'] = userid[0]

        self.log("登陆数据:" + str(_login_dict))
        # 响应Cookie
        cookie1 = response.headers.getlist('Set-Cookie')

        self.log("后台首次写入的响应Cookies：:" + str(cookie1))
        yield FormRequest(url=POST_LOGIN, formdata=_login_dict,
                          meta={'cookiejar': response.meta['cookiejar']},
                          callback=self.check_login)

    def check_login(self, response):
        cookie2 = response.request.headers.getlist('Cookie')
        self.log('登录时携带请求的Cookies：' + str(cookie2))
        yield Request(url=JYEOO_INDEX, meta={'cookiejar': True}, callback=self.jyeoo_index_parse)

    def jyeoo_index_parse(self, response):
        cookie3 = response.request.headers.getlist('Cookie')
        db_dict = dict()
        db_dict['create_time'] = datetime.datetime.now()

        if len(cookie3) > 0 and cookie3[0]:
            self.is_login = True
            db_dict['cookie'] = cookie3[0].decode("utf-8")
            # cookie_dict = CookieStrToDict(Cookie3[0].decode("utf-8"))
        self.log('查看需要登录才可以访问的页面携带Cookies：' + str(cookie3))
        # 判断是否登陆成功和cookie是否获取成功
        user_info = response.css('.user').xpath('./span/text()').extract_first()

        if user_info and self.is_login:
            self.log('登陆成功!登陆账号:' + user_info)
            self.log(db_dict['cookie'])
            self.db_session.add(CookieInfo(**db_dict))
            for url in start_urls:
                yield scrapy.Request(url=url, cookies=db_dict['cookie'], meta={'cookiejar': True}, callback=self.parse)

    def parse(self, response):
        # 开始爬取
        self.log("开始爬取 url:" + str(response.url))
        # 解析数据
        sss = JyeooItem()
        yield sss
        # 开始进行分页操作
