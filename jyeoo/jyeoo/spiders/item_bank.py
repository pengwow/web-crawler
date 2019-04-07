# -*- coding:utf-8 -*-
from jyeoo.items import ItemBankItem
import requests
from jyeoo.common.constant import DETAIL_PAGE, POINTCARD_PAGE
from urllib.parse import quote
import scrapy
from mako.template import Template
import logging
from scrapy import FormRequest, Request
from jyeoo.settings import JYEEO_USER, JYEOO_PASSWORD, SPLASH_URL
from scrapy.http.cookies import CookieJar
from jyeoo.common.utils import get_valid_cookie, get_item_bank_url, cookie_str_to_list, cookie_str_to_dict
from jyeoo.model import DBSession, CookieInfo
import datetime
from jyeoo.common.constant import STR
from scrapy_splash import SplashRequest  # , SplashFormRequest
import json
from queue import Queue

LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"
LOGIN_POST_URL = 'http://api.jyeoo.com/home/login?ReturnUrl=%2F'
JYEOO_INDEX = "http://www.jyeoo.com"

"""
LUA函数
"""
click_script = """
function main(splash)
    -- ...
    local element = splash:select('//a[@class="next"]')
    local bounds = element:bounds()
    assert(element:mouse_click{x=bounds.width/2, y=bounds.height/2})
    -- ...
end
"""
# 获取cookie函数
get_cookie_script = """
function main(splash, args)
  local json = require("json")
  local response = splash:http_post{url="${login_url}",     
      body=json.encode({Email="${Email}",Sn="",Password='${Password}',UserID='${UserID}'}),
      headers={["content-type"]="application/json"}
    }
    splash:wait(0.5)
    splash:go("http://www.jyeoo.com")
    splash:wait(0.5)
    return {
    cookies = splash:get_cookies()
    }
end
"""
# 获取题库,以及翻页
scroll_script = """
function main(splash,args)
    % for item in cookies:
    splash:add_cookie{"${item['key']}", "${item['value']}", "/", domain=".jyeoo.com"}
    % endfor
    splash:set_viewport_size(1028, 10000)
    splash:go(args.url)
    splash.scroll_position={0,2000}
    splash:wait(0.5)
    --splash:wait(0.5)
    --splash:set_viewport_full()
    --splash:wait(1)
    % if next:
    splash:evaljs('javascript:goPage(${next_index},this)')
    splash:wait(0.5)
    --local element = splash:select('.next')
    --local bou nds = element:bounds()
    --assert(element:mouse_click{x=bounds.width/3, y=bounds.height/3})
    --splash:wait(1)
    % endif
    return splash:html()
end
"""


class ItemBank(scrapy.Spider):
    name = "item_bank"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()
    point_queue = Queue()
    # 是否登陆
    is_login = False

    cookie = None
    db_session = DBSession()
    start_urls = dict()

    error_page_list = list()  # TODO: 待完成错误页的处理

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie(STR)
        self.start_urls = get_item_bank_url()
        if not cookie:
            self.log("未获取到cookie!,开始登陆获取cookie")
            yield SplashRequest(url=LOGIN_URL, meta={'cookiejar': True}, callback=self.login_parse)
        else:
            self.log("使用缓存的cookie,进行爬取")
            script_t = Template(scroll_script)
            new_scroll_script = script_t.render(cookies=cookie_str_to_list(cookie), next=False)
            self.log(new_scroll_script)
            cookie_dict = cookie_str_to_dict(cookie)
            for item in self.start_urls.keys():
                url = self.start_urls.get(item)['url']
                self.log("爬虫开始爬取 url:" + url)
                yield SplashRequest(url=url,
                                    endpoint="execute",
                                    cookies=cookie_dict,
                                    meta={'cookiejar': True,
                                          'lua_source': new_scroll_script,
                                          'jyeoo_args': self.start_urls.get(item),
                                          'jyeoo_cookie_str': cookie,
                                          'cookies': cookie_dict
                                          },
                                    args={'wait': '0.5',
                                          "render_all": 1,
                                          'lua_source': new_scroll_script},
                                    callback=self.parse)

    def login_parse(self, response):
        _login_dict = dict()
        _login_dict['Sn'] = ''
        userid = response.css('#UserID::attr(value)').extract()

        _login_dict['Email'] = JYEEO_USER

        _login_dict['Password'] = JYEOO_PASSWORD
        if len(userid) > 0:
            _login_dict['UserID'] = userid[0]

        self.log("登陆数据:" + str(_login_dict))
        # 响应Cookie
        cookie1 = response.headers.getlist('Set-Cookie')
        cookie_t = Template(get_cookie_script)
        _login_dict['login_url'] = LOGIN_POST_URL
        new_cookie_script = cookie_t.render(**_login_dict)
        self.log("后台首次写入的响应Cookies：:" + str(cookie1))
        print(new_cookie_script)
        get_cookie_url = SPLASH_URL + 'execute?lua_source=' + quote(new_cookie_script)

        splash_response = requests.get(get_cookie_url)

        cookie_dict = json.loads(splash_response.text)
        db_dict = dict()
        cookie_str = '{name}={value}'
        new_cookie_str = ''
        if cookie_dict.get('cookies'):
            db_dict['create_time'] = datetime.datetime.now()
            for cookie in cookie_dict.get('cookies'):
                new_cookie_str = new_cookie_str + cookie_str.format(**cookie) + ';'

            db_dict['cookie'] = new_cookie_str[:-1]
            self.db_session.add(CookieInfo(**db_dict))

    def check_login(self, response):
        cookie2 = response.request.headers.getlist('Cookie')
        self.log('登录时携带请求的Cookies：' + str(cookie2))
        yield SplashRequest(url=JYEOO_INDEX, meta={'cookiejar': True}, callback=self.jyeoo_index_parse)

    def jyeoo_index_parse(self, response):
        cookie3 = response.request.headers.getlist('Cookie')
        db_dict = dict()
        db_dict['create_time'] = datetime.datetime.now()

        if len(cookie3) > 0 and cookie3[0]:
            self.is_login = True
            db_dict['cookie'] = cookie3[0].decode("utf-8")
            # cookie_dict = cookie_str_to_dict(Cookie3[0].decode("utf-8"))
        self.log('查看需要登录才可以访问的页面携带Cookies：' + str(cookie3))
        # 判断是否登陆成功和cookie是否获取成功
        user_info = response.css('.user').xpath('./span/text()').extract_first()
        self.log(user_info)
        if user_info and self.is_login:
            self.log('登陆成功!登陆账号:' + user_info)
            self.log(db_dict['cookie'])
            self.db_session.add(CookieInfo(**db_dict))
            # 重新开始
            self.start_requests()
            # for url in start_urls:
            #     yield scrapy.Request(url=url, cookies=db_dict['cookie'],
            # meta={'cookiejar': True}, callback=self.parse)

    def parse(self, response):
        # 开始爬取
        jyeoo_args = response.meta.get('jyeoo_args')
        response.meta.get('jyeoo_args')

        subject = jyeoo_args.get('subject')
        cookies = response.meta['splash']['args']['cookies']
        fieldset = response.xpath('.//fieldset')
        for item in fieldset:
            fieldset_id = item.xpath('./@id').get()
            detail_page_url = DETAIL_PAGE.format(subject=subject, fieldset=fieldset_id)
            print(detail_page_url)
            # 解析详情页数据
            yield scrapy.Request(url=detail_page_url, meta={'cookiejar': True,
                                                            'jyeoo_args': jyeoo_args,
                                                            'fieldset_id': fieldset_id
                                                            },
                                 cookies=cookies,
                                 callback=self.detail_page_parse)

        # 获取当前页
        index_cur = response.xpath('//a[@class="index cur"]/text()').get()
        # 获取总页
        all_index = response.xpath('//select[@class="ml10"]/option[last()]/@value').get()
        if index_cur and index_cur.isdigit() and all_index and all_index.isdigit():
            next_index = int(index_cur) + 1
            # 当前页小于总页数,可以翻页
            if next_index < int(all_index):
                jyeoo_cookie_str = response.meta.get('jyeoo_cookie_str')
                # 渲染滚动题库页面翻页
                script_t = Template(scroll_script)
                new_scroll_script = script_t.render(cookies=cookie_str_to_list(jyeoo_cookie_str),
                                                    next=True,
                                                    next_index=str(next_index))
                # 开始进行翻页操作
                yield SplashRequest(url=response.url,
                                    endpoint="execute",
                                    cookies=cookies,
                                    meta={'cookiejar': True,
                                          'lua_source': new_scroll_script,
                                          'jyeoo_args': jyeoo_args,
                                          'cookies': cookies
                                          },
                                    args={'wait': '0.5',
                                          "render_all": 1,
                                          'lua_source': new_scroll_script},
                                    callback=self.parse)

    def is_error_page(self, response):
        """
        判断当前页是错误页,插入错误页列表.之后处理
        :param response:
        :return:
        """
        erros = response.xpath('//div[@class="erros"]/text()').get()
        if erros:
            if -1 != erros.find('请稍后再查看'):
                temp_dict = dict()
                temp_dict['url'] = response.url
                temp_dict['jyeoo_args'] = response.meta.get('jyeoo_args')
                self.error_page_list.append(temp_dict)
                self.log("爬取失败:{url}".format(url=response.url), logging.ERROR)
                return True
        return False

    def get_pointcard(self, response):
        """
        获取知识点
        :param item_id: xpath路径
        :param pointcard_xpath: xpath路径
        :return:
        """
        item_id = response.meta.get('fieldset_id')
        chaper_id = response.meta.get('jyeoo_args').get('chaper_id')
        pointcard_xpath = response.xpath('//div[@class="pt3"]')
        point_a = pointcard_xpath.xpath('.//a')
        result = list()
        for item in point_a:
            onclick = item.xpath('./@onclick').get('')
            onclick = onclick.split(';')[0].split('openPointCard')[1]
            onclick = onclick.replace("'", "").replace('"', '').replace('(', "").replace(")", "")
            pointcard = onclick.split(',')
            pointcard_page = POINTCARD_PAGE.format(subject=pointcard[0],
                                                   point_code=pointcard[1])
            print(pointcard_page)
            result.append(dict(url=pointcard_page,
                               item_id=item_id,
                               point_code=pointcard[1],
                               subject=pointcard[0],
                               chaper_id=chaper_id))

        return result

    def pointcard_parse(self, response):
        fieldset_id = requests.meta.get('fieldset_id')
        li = response.xpath('//ul/li')
        for item in li:
            title = item.xpath('./text()').get()
            print(title)
        return

    def detail_page_parse(self, response):
        if self.is_error_page(response):
            return
        jyeoo_args = response.meta.get('jyeoo_args')
        print(jyeoo_args)
        bank_item = ItemBankItem()
        bank_item['library_id'] = jyeoo_args.get('library_id')
        bank_item['chaper_id'] = jyeoo_args.get('chaper_id')
        bank_item['field_code'] = jyeoo_args.get('field_code')
        bank_item['from_code'] = jyeoo_args.get('subject')

        bank_item['difficult_code'] = ''
        bank_item['year_code'] = ''
        bank_item['used_times'] = ''
        bank_item['exam_times'] = ''
        bank_item['year_area'] = ''

        item_id = response.meta.get('fieldset_id')
        fieldset_xpath = '//div[@id="{fieldset_id}"]'.format(fieldset_id=item_id)
        detail_data = response.xpath(fieldset_xpath)
        # 考题
        bank_item['context'] = detail_data.xpath('.//div[@class="pt1"]').get()
        # 选择区/答题区/简答区
        pt2 = detail_data.xpath('.//div[@class="pt2"]').get('')
        bank_item['context'] = bank_item['context'] + pt2
        # 考点
        pt3 = detail_data.xpath('.//div[@class="pt3"]').get('')
        # 获取知识点内容
        pointcard_xpath = detail_data.xpath('.//div[@class="pt3"]')
        bank_item['point'] = self.get_pointcard(response)
        # 专题
        pt4 = detail_data.xpath('.//div[@class="pt4"]').get('')
        # 分析
        pt5 = detail_data.xpath('.//div[@class="pt5"]').get('')
        # 解答
        pt6 = detail_data.xpath('.//div[@class="pt6"]').get('')
        # 点评
        pt7 = detail_data.xpath('.//div[@class="pt7"]').get('')
        # pt9 = detail_data.xpath('.//div[@class="pt9"]').get()
        bank_item['anwser'] = pt3 + pt4 + pt5 + pt6 + pt7
        fieldtip_left = detail_data.xpath('.//div[@class="fieldtip-left"]')
        record_time = fieldtip_left.xpath('.//span[1]/text()').get()
        used_times = fieldtip_left.xpath('.//span[2]/text()').get()
        exam_times = fieldtip_left.xpath('.//span[3]/text()').get()
        difficult_code = fieldtip_left.xpath('.//span[4]/text()').get()
        if record_time:
            bank_item['record_time'] = record_time.replace("：", ":").split(':')[1]
        if used_times:
            bank_item['used_times'] = used_times.replace("：", ":").split(':')[1]
        if exam_times:
            bank_item['exam_times'] = exam_times.replace("：", ":").split(':')[1]
        if difficult_code:
            bank_item['difficult_code'] = difficult_code.replace("：", ":").split(':')[1]
        # with open('E:\\Temp\\aaa.html','w+',encoding="utf-8") as DD:
        #     DD.write(response.text)
        yield bank_item
