# -*- coding:utf-8 -*-

def CookieStrToDict(cookies):
    itemDict = {}
    items = cookies.split(';')
    for item in items:
        arr = item.split('=')
        key = arr[0].replace(' ', '')
        value = arr[1]
        itemDict[key] = value
    return itemDict


def get_valid_cookie():
    from jyeoo.model import DBSession, CookieInfo
    session = DBSession()
    cookie_query = session.session.query(CookieInfo).filter(CookieInfo.is_valid == True)
    for item in cookie_query:
        return CookieStrToDict(item.cookie)
    return None


def get_chapter_url():
    from jyeoo.mysql_model import DBSession, LibraryEntry
    re_list = list()
    session = DBSession()
    query = session.session.query(LibraryEntry).all()
    for item in query:
        url_str = 'http://www.jyeoo.com/{subject}/ques/search?f=0&q={id}'
        if int(item.level_code) > 1:
            re_list.append(
                url_str.format(subject=item.subject_code + item.level_code, id=item.id)
            )
        else:
            re_list.append(
                url_str.format(subject=item.subject_code, id=item.id)
            )
    return re_list


def get_item_bank_url():
    return

