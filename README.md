# 菁优网爬虫[中止]
使用另外分支-项目https://github.com/pengwow/jyeoo-crawler-gui
## 说明

* jyeoo 为第一版爬虫基于scrapy + splash 

1.账号使用api.jyeoo.com后台接口自动登陆
由于账号被封，此方法废弃，改用手动登陆获取cookie方式

2.vip账号爬取次数过多发生被封号，爬取次数规则未摸清

3.jyeoo后台检测机制使账号发生课题和解析内容不一致，即课题id为假数据
经客服解决，故无法实现全自动爬取


## 代码参考

* splash部署采用docker方式，详见官方文档

* splash的动态渲染，翻页，触发按钮，执行js等采用lua脚本执行

lua脚本采用mako模板用来动态生成
``` python
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
```

* 爬取章节目前已爬取有效数据4万+条  library_chapter.py	


