# -*- coding:utf-8 -*-
from common.constant import *


def cookie_str_to_list(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""

    # if fixed_key:
    "[{'key': 'aaaa', 'value': 'dddd'}, {'key': 'sss', 'value': 'eeeee'}]"
    # key_dict = cookie_str_to_dict(cookie)
    # cookies = list()
    key_dict = [l.split("=", 1) for l in cookie.replace(" ", "").split(";")]
    # print(key_dict)
    cookies = [dict(key=item[0], value=item[1]) for item in key_dict]

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


def get_valid_cookie(re_type=DICT):
    """
    获取有效的cookie
    :param re_type:返回类型
    :return:
    """
    from jyeoo.model import DBSession, CookieInfo
    session = DBSession()
    cookie_query = session.session.query(CookieInfo).filter(CookieInfo.is_valid == 1)
    for item in cookie_query:
        if isinstance(re_type, dict):
            return cookie_str_to_dict(item.cookie)
        if isinstance(re_type, str):
            return item.cookie
        if isinstance(re_type, list):
            return cookie_str_to_list(item.cookie)
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


def get_item_bank_url():
    from jyeoo.mysql_model import DBSession, LibraryChapter, LibraryEntry, ItemStyle
    # re_list = list()
    re_dict = dict()
    session = DBSession()
    query = session.session.query(LibraryChapter).all()
    url_str = 'http://www.jyeoo.com/{subject}/ques/search?f=0&q={pk}&ct={item_style_code}&fg={field_code}'
    fgs = ['8', '4', '2', '16']
    # 遍历章节
    for item in query:
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
                        re_dict[item.id] = temp_dict
    return re_dict
