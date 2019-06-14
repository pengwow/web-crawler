from jyeoo.settings import  SPLASH_URL, JYEOO_USERID
from mako.template import Template
from urllib.parse import quote
import requests
import json
import datetime
LOGIN_POST_URL = 'http://api.jyeoo.com/home/login?ReturnUrl=%2F'
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

JYEEO_USER = '726617867@qq.com'
JYEOO_PASSWORD = 'gshare365'
JYEOO_USERID = '88888888-8888-8888-8888-888888888888'

def login_parse():
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

ddd = login_parse()
print(ddd)