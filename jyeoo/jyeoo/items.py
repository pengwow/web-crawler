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


class LevelSubjectsItem(scrapy.Item):
    id = scrapy.Field()
    level_name = scrapy.Field()
    level_code = scrapy.Field()
    subject_name = scrapy.Field()
    subject_code = scrapy.Field()
    search_url = scrapy.Field()


class LevelGradeItem(scrapy.Item):
    id = scrapy.Field()
    level_name = scrapy.Field()
    level_code = scrapy.Field()
    grade_name = scrapy.Field()
    grade_code = scrapy.Field()
