# -*- coding:utf-8 -*-


def CookieStrToDict(cookies):
    itemDict = {}
    items = cookies.split(';')
    for item in items:
        arr=item.split('=')
        key = arr[0].replace(' ', '')
        value = arr[1]
        itemDict[key] = value
    return itemDict

def get_valid_cookie():
    from jyeoo.model import DBSession, CookieInfo
    session = DBSession()
    cookie_query = session.session.query(CookieInfo).filter(CookieInfo.is_valid==True)
    for item in cookie_query:
        return CookieStrToDict(item.cookie)
    return None