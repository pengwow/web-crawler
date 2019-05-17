# -*- coding:utf-8 -*-
import datetime
from mako.template import Template
import requests
from jyeoo.common.constant import *
import json
from urllib.parse import quote
import sys


def cookie_str_to_list(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = list()
    try:
        # if fixed_key:
        "[{'key': 'aaaa', 'value': 'dddd'}, {'key': 'sss', 'value': 'eeeee'}]"
        # key_dict = cookie_str_to_dict(cookie)
        # cookies = list()
        key_dict = [l.split("=", 1) for l in cookie.replace(" ", "").split(";")]
        # print(key_dict)
        cookies = [dict(key=item[0], value=item[1]) for item in key_dict]
    except Exception as cookie:
        print(cookie)
    # for key, value in key_dict:
    #     new_dict = dict(key=key, value=value)
    #     cookies.append(new_dict)
    # else:
    #     "{'aaaa': 'dddd', 'sss': 'eeeee'}"
    #     cookies = dict([l.split("=", 1) for l in cookie.split(";")])
    return cookies


def cookie_str_to_dict(cookies):
    # item_dict = {}
    # items = cookies.split(';')
    item_dict = dict([l.split("=", 1) for l in cookies.replace(" ", "").split(";")])
    # for item in items:
    #     arr = item.split('=')
    #     key = arr[0].replace(' ', '')
    #     value = arr[1]
    #     item_dict[key] = value
    return item_dict


def login_parse():
    # vfrom jyeoo.model import DBSession, CookieInfo
    from jyeoo.settings import JYEEO_USER, JYEOO_PASSWORD, SPLASH_URL, JYEOO_USERID
    _login_dict = dict()
    _login_dict['Sn'] = ''
    # userid = response.css('#UserID::attr(value)').extract()

    _login_dict['Email'] = JYEEO_USER

    _login_dict['Password'] = JYEOO_PASSWORD
    _login_dict['UserID'] = JYEOO_USERID
    # if len(userid) > 0:
    #     _login_dict['UserID'] = userid[0]

    # self.log("登陆数据:" + str(_login_dict))
    # 响应Cookie
    # cookie1 = response.headers.getlist('Set-Cookie')
    cookie_t = Template(get_cookie_script)
    _login_dict['login_url'] = LOGIN_POST_URL
    new_cookie_script = cookie_t.render(**_login_dict)
    # self.log("后台首次写入的响应Cookies：:" + str(cookie1))
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
        # db_session = DBSession()
        # db_session.add(CookieInfo(**db_dict))
        return db_dict['cookie']
    return None


def get_valid_cookie(re_type=DICT):
    """
    获取有效的cookie
    :param re_type:返回类型
    :return:
    """
    from jyeoo.mysql_model import DBSession, CookieInfo
    session = DBSession()
    cookie_query = session.session.query(CookieInfo).filter(CookieInfo.is_valid == 1)
    cookie_str = cookie_query[0].cookie
    # 调用api网址获取cookie
    # cookie_str = login_parse()
    # for item in cookie_query:
    if isinstance(re_type, dict):
        return cookie_str_to_dict(cookie_str)
        # return cookie_str_to_dict(item.cookie)
    if isinstance(re_type, str):
        return cookie_str
        # return item.cookie
    if isinstance(re_type, list):
        return cookie_str_to_list(cookie_str)
        # return cookie_str_to_list(item.cookie)
    return None


def get_chapter_url():
    from jyeoo.mysql_model import DBSession, LibraryEntry
    # re_list = list()
    re_dict = dict()
    session = DBSession()
    query = session.session.query(LibraryEntry).all()
    for item in query:
        url_str = 'http://www.jyeoo.com/{subject}/ques/search?f=0&q={id}'
        if int(item.level_code) > 1:
            re_dict[item.id] = url_str.format(subject=item.subject_code + item.level_code, id=item.id)
        else:
            re_dict[item.id] = url_str.format(subject=item.subject_code, id=item.id)
    return re_dict


def get_chapter_point_url():
    """
    获取知识点url列表
    :return:
    """
    from jyeoo.mysql_model import DBSession, ChaperPoint
    session = DBSession()
    chaper_point_query = session.session.query(ChaperPoint).filter(ChaperPoint.content.is_(None))
    re_list = list()
    for item in chaper_point_query:
        temp_dict = dict()
        temp_dict['url'] = item.url
        temp_dict['id'] = item.id
        re_list.append(temp_dict)
    return re_list


def get_item_bank_url():
    """
    获取题库url列表用来爬取数据
    :return:
    """
    from jyeoo.mysql_model import DBSession, LibraryChapter, LibraryEntry, ItemStyle, ItemBank
    from jyeoo.settings import ITEM_BANK_MAX_COUNT
    # re_list = list()

    re_dict = dict()
    session = DBSession()

    query = session.session.query(LibraryChapter).all()
    url_str = 'http://www.jyeoo.com/{subject}/ques/search?f=0&q={pk}&ct={item_style_code}&fg={field_code}'
    fgs = ['8', '4', '2', '16']
    # 遍历章节
    for item in query:
        today_count = session.session.query(ItemBank).filter(
            ItemBank.create_date == datetime.datetime.now().strftime('%Y-%m-%d')).count()
        if today_count >= ITEM_BANK_MAX_COUNT:
            # 超过每日最大数量限制
            sys.exit(0)
        entry_query = session.session.query(LibraryEntry).filter(LibraryEntry.id == item.library_id)
        # 遍历 题库索引
        for entry_item in entry_query:
            style_query = session.session.query(ItemStyle).filter(ItemStyle.subject_code == entry_item.subject_code,
                                                                  ItemStyle.level_code == entry_item.level_code)
            if int(entry_item.level_code) > 1:
                # 修改subject学科 拼接
                subject = entry_item.subject_code + entry_item.level_code
            else:
                subject = entry_item.subject_code
            # 遍历题型 选择...解答...
            for style_item in style_query:
                # 遍历题类 常考,易错,好题,压轴
                for fg in fgs:
                    temp_dict = dict()
                    # 学科
                    temp_dict['subject'] = subject
                    # 教材ID
                    temp_dict['library_id'] = item.library_id
                    # 章节ID
                    temp_dict['chaper_id'] = item.id
                    # 章节直连
                    temp_dict['pk'] = item.pk
                    # 题型
                    temp_dict['item_style_code'] = style_item.style_code
                    # 题类
                    temp_dict['field_code'] = fg
                    temp_dict['url'] = url_str.format(**temp_dict)
                    # 已经爬取过了则跳过
                    item_bank_count = session.session.query(ItemBank).filter(ItemBank.url == temp_dict['url']).count()
                    if item_bank_count > 0:
                        print('已经爬取了%s' % temp_dict['url'])
                        continue
                    re_dict[item.id] = temp_dict
                    yield re_dict


# 取字符串中两个符号之间的东东
def txt_wrap_by(start_str, end, html):
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()
