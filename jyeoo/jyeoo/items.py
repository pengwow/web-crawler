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


class LibraryChapterItem(scrapy.Item):
    id = scrapy.Field()
    library_id = scrapy.Field()
    name = scrapy.Field()
    parent_id = scrapy.Field()
    pk = scrapy.Field()


class ItemBankItem(scrapy.Item):
    # 主键 UUID
    id = scrapy.Field()
    # 教材ID
    library_id = scrapy.Field()
    # 章节ID
    chaper_id = scrapy.Field()
    # 题型
    item_style_code = scrapy.Field()
    # 难度编码
    difficult_code = scrapy.Field()
    # 题类编码
    field_code = scrapy.Field()
    # 来源编码
    from_code = scrapy.Field()
    # 年份编码
    year_code = scrapy.Field()
    # 组卷次数
    used_times = scrapy.Field()
    # 真题次数
    exam_times = scrapy.Field()
    # 试题内容
    context = scrapy.Field()
    # 试题解析
    anwser = scrapy.Field()
    # 年份与地区
    year_area = scrapy.Field()
    # 收录时间
    record_time = scrapy.Field()

    # 知识点 dict()需解析到知识点表
    point = scrapy.Field()

