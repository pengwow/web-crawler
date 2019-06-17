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

* 爬取章节目前已爬取有效数据4万+条


