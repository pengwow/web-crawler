# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JyeooItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JyeooLoginItem(scrapy.Item):
    email = scrapy.Field()
    password = scrapy.Field()
    userid = scrapy.Field()


