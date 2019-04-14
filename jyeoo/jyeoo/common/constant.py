# -*- coding:utf-8 -*-
"""
常量
"""
STR = str()
DICT = dict()
LIST = list()

# 详情页面
DETAIL_PAGE = 'http://www.jyeoo.com/{subject}/ques/detail/{fieldset}'

# 知识点页面
POINTCARD_PAGE = 'http://www.jyeoo.com/{subject}/api/pointcard?a={point_code}'
LOGIN_URL = 'http://api.jyeoo.com'

POST_LOGIN = "http://api.jyeoo.com/home/login?ReturnUrl=%2F%2F%2FScripts%2Fapi.js"
LOGIN_POST_URL = 'http://api.jyeoo.com/home/login?ReturnUrl=%2F'
JYEOO_INDEX = "http://www.jyeoo.com"
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


start_urls = [
    'http://www.jyeoo.com/math3/ques/search?f=0',
    # 'http://www.jyeoo.com/chinese3/ques/search?f=0',
    # 'http://www.jyeoo.com/english3/ques/search?f=0',
    # 'http://www.jyeoo.com/math0/ques/search?f=1',
    # 'http://www.jyeoo.com/math/ques/search?f=0',
    # 'http://www.jyeoo.com/physics/ques/search?f=0',
    # 'http://www.jyeoo.com/chemistry/ques/search?f=0',
    # 'http://www.jyeoo.com/bio/ques/search?f=0',
    # 'http://www.jyeoo.com/geography/ques/search?f=0',
    # 'http://www.jyeoo.com/chinese/ques/search?f=0',
    # 'http://www.jyeoo.com/english/ques/search?f=0',
    # 'http://www.jyeoo.com/politics/ques/search?f=0',
    # 'http://www.jyeoo.com/history/ques/search?f=0',
    # 'http://www.jyeoo.com/math2/ques/search?f=0',
    # 'http://www.jyeoo.com/physics2/ques/search?f=0',
    # 'http://www.jyeoo.com/chemistry2/ques/search?f=0',
    # 'http://www.jyeoo.com/bio2/ques/search?f=0',
    # 'http://www.jyeoo.com/geography2/ques/search?f=0',
    # 'http://www.jyeoo.com/chinese2/ques/search?f=0',
    # 'http://www.jyeoo.com/english2/ques/search?f=0',
    # 'http://www.jyeoo.com/politics2/ques/search?f=0',
    # 'http://www.jyeoo.com/history2/ques/search?f=0',
    # 'http://www.jyeoo.com/tech1/ques/search?f=0',
    # 'http://www.jyeoo.com/tech2/ques/search?f=0'
]
