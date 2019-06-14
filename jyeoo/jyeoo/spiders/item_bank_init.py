# -*- coding:utf-8 -*-
import os
import signal
from jyeoo.items import ItemBankInitItem
from jyeoo.common.constant import DETAIL_PAGE
from jyeoo.mysql_model import DBSession,CookieInfo
import scrapy
import random
from mako.template import Template
from jyeoo.settings import ITEM_BANK_INIT_MAX_COUNT
from scrapy.http.cookies import CookieJar
from jyeoo.common.utils import get_valid_cookie, get_item_bank_init_url, cookie_str_to_list, cookie_str_to_dict

from jyeoo.common.constant import STR
from scrapy_splash import SplashRequest

LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"
LOGIN_POST_URL = 'http://api.jyeoo.com/home/login?ReturnUrl=%2F'
JYEOO_INDEX = "http://www.jyeoo.com"

"""
LUA函数
"""
# 获取cookie函数
get_cookie_script = """
function main(splash, args)
  local json = require("json")
  local response = splash:http_post{url="${login_url}",     
      body=json.encode({Email="${Email}",Sn="",Password='${Password}',UserID='${UserID}'}),
      headers={["content-type"]="application/json"}
    }
    splash:wait(1)
    splash:go("http://www.jyeoo.com")
    splash:wait(2)
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
    splash:wait(${sleep})
    % if next:
    splash:evaljs('javascript:goPage(${next_index},this)')
    splash:wait(1)
    % endif
    return splash:html()
end
"""


class ItemBank(scrapy.Spider):
    name = "item_bank_init"
    # 实例化一个cookiejar对象
    cookie_jar = CookieJar()

    # 是否登陆
    is_login = False

    cookie = None
    db_session = DBSession()
    start_urls = dict()
    requests_number = 0
    error_page_list = list()  # TODO: 待完成错误页的处理

    def start_requests(self):  # 由此方法通过下面链接爬取页面
        cookie = get_valid_cookie(STR)
        self.start_urls = get_item_bank_init_url()
        if not cookie:
            self.log("未获取到cookie!,开始登陆获取cookie")
        else:

            for start_urls in self.start_urls:
                cookie = get_valid_cookie(STR)
                self.log("使用缓存的cookie,进行爬取")
                if not cookie:
                    break
                script_t = Template(scroll_script)
                new_scroll_script = script_t.render(cookies=cookie_str_to_list(cookie), sleep=random.randint(15, 20),
                                                    next=False)
                self.log(new_scroll_script)
                cookie_dict = cookie_str_to_dict(cookie)
                for item in start_urls.keys():
                    url = start_urls.get(item)['url']
                    self.log("爬虫开始爬取 url:" + url)
                    yield SplashRequest(url=url,
                                        endpoint="execute",
                                        cookies=cookie_dict,
                                        meta={'cookiejar': True,
                                              'lua_source': new_scroll_script,
                                              'jyeoo_args': start_urls.get(item),
                                              'jyeoo_cookie_str': cookie,
                                              'cookies': cookie_dict
                                              },
                                        args={'wait': '0.5',
                                              "render_all": 1,
                                              'lua_source': new_scroll_script},
                                        callback=self.parse)

    def parse(self, response):
        cookies = response.meta['splash']['args']['cookies']
        # 开始爬取
        self.requests_number += 1
        if self.requests_number >= ITEM_BANK_INIT_MAX_COUNT:

            query = self.db_session.session.query(CookieInfo).filter(CookieInfo.cookie==cookies)
            query.is_valid = 0
            self.db_session.session.commit()
            return
            # pid = os.getpid()
            # os.kill(pid, signal.SIGKILL)
            # raise Exception(
            #     '超出设置的最大上线 {max_count} , 当前执行数量{requests_number} '.format(max_count=ITEM_BANK_INIT_MAX_COUNT,
            #                                                               requests_number=self.requests_number))
        jyeoo_args = response.meta.get('jyeoo_args')
        subject = jyeoo_args.get('subject')
        library_id = jyeoo_args.get('library_id')
        chaper_id = jyeoo_args.get('chaper_id')
        # from_code = jyeoo_args.get('subject')
        item_style_code = jyeoo_args.get('item_style_code')

        fieldset = response.xpath('.//fieldset')
        for item in fieldset:
            fieldset_id = item.xpath('./@id').get()
            if not fieldset_id or fieldset_id == '00000000-0000-0000-0000-000000000000':
                self.log('获取ID错误: %s' % response.url)
                continue
            self.log('页面: %s' % response.url)
            detail_page_url = DETAIL_PAGE.format(subject=subject, fieldset=fieldset_id)
            # print(detail_page_url)
            self.log(detail_page_url)
            # print(str(fieldset_count)+'   '+fieldset_id)
            item_init = ItemBankInitItem()
            item_init['from_code'] = subject
            item_init['item_style_code'] = item_style_code
            item_init['library_id'] = library_id
            item_init['chaper_id'] = chaper_id
            item_init['fieldset_id'] = fieldset_id
            item_init['detail_page_url'] = detail_page_url
            item_init['ques_url'] = response.url
            yield item_init

        # 获取当前页
        index_cur = response.xpath('//a[@class="index cur"]/text()').get()
        # 获取总页
        all_index = response.xpath('//select[@class="ml10"]/option[last()]/@value').get()
        if index_cur and index_cur.isdigit() and all_index and all_index.isdigit():
            next_index = int(index_cur) + 1
            # 当前页小于总页数,可以翻页
            if next_index < int(all_index):
                jyeoo_cookie_str = response.meta.get('jyeoo_cookie_str')
                # print(jyeoo_cookie_str)
                self.log(jyeoo_cookie_str)
                # 渲染滚动题库页面翻页
                script_t = Template(scroll_script)
                new_scroll_script = script_t.render(cookies=cookie_str_to_list(jyeoo_cookie_str),
                                                    next=True,
                                                    sleep=random.randint(15, 20),
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
