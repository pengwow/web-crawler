# -*- coding:utf-8 -*-
from jyeoo.items import JyeooLoginItem
import scrapy
from scrapy import FormRequest, Request
from jyeoo.settings import JYEEO_USER,JYEOO_PASSWORD
import logging
import requests
from jyeoo.common.constant import start_urls

LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/math3/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"

JYEOO_INDEX = "http://www.jyeoo.com/"

class jyeoo(scrapy.Spider):
    name = "jyeoo"
    login_headers = {
        "Host": "api.jyeoo.com",
        "Referer": "http://api.jyeoo.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    headers = {
        'Host':'www.jyeoo.com',
        'Referer':'http://www.jyeoo.com/',
        'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }

    # 是否登陆
    is_login = False

    cookie = None

    def start_requests(self): # 由此方法通过下面链接爬取页面
        
        # 定义爬取的链接
        urls = [
            'http://api.jyeoo.com/',# 用于登陆
            
        ]
        for url in urls:
            if self.is_login:
                self.log("爬虫开始爬取 url:" + url)
                yield scrapy.Request(url=url,meta={'cookiejar':True},callback=self.parse)
            else:
                self.log("未登录进行登陆操作!")
                # 登陆获取cookie
                yield scrapy.Request(url=url,meta={'cookiejar':1}, callback=self.login_parse) #爬取到的页面如何处理？提交给parse方法处理

    def login_parse(self,response):
        _login_dict = dict()
        _login_dict['Sn'] = ''
        #email = response.css('#Email::attr(value)').extract()
        #password = response.css('#Password::attr(value)').extract()
        userid = response.css('#UserID::attr(value)').extract()

        _login_dict['Email'] = JYEEO_USER

        _login_dict['Password'] = JYEOO_PASSWORD
        if len(userid) > 0:
            _login_dict['UserID'] = userid[0]
        
        self.log("登陆数据:"+str(_login_dict))
        # 响应Cookie
        Cookie1 = response.headers.getlist('Set-Cookie')

        self.log("后台首次写入的响应Cookies：:" + str(Cookie1))
        yield FormRequest(url=POST_LOGIN,formdata=_login_dict,
        headers=self.login_headers,
        meta={'cookiejar':response.meta['cookiejar']},
        callback=self.check_login)

    def check_login(self,response):
        Cookie2 = response.request.headers.getlist('Cookie')
        self.log('登录时携带请求的Cookies：'+str(Cookie2))
        yield Request(url=JYEOO_INDEX,meta={'cookiejar':True},callback=self.jyeoo_index_parse)

    def jyeoo_index_parse(self,response):
        Cookie3 = response.request.headers.getlist('Cookie')
        if Cookie3:
            self.is_login = True
        self.log('查看需要登录才可以访问的页面携带Cookies：'+str(Cookie3))
        # 判断是否登陆成功和cookie是否获取成功
        user_info = response.css('.user').xpath('./span/text()').extract_first()
        self.log(user_info)
        if user_info and self.is_login:
            self.log('登陆成功!登陆账号:'+user_info)
            
            for url in start_urls:
                yield scrapy.Request(url=url,callback=self.parse,meta={'cookiejar':True})
        else:
            self.log('获取登陆用户失败',level=logging.ERROR)
        
    def parse(self, response):
        # 开始爬取
        self.log("开始爬取 url:" + str(response.url))
        # 解析数据
        
        # 开始进行分页操作
    



        