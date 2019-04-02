# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JyeooPipeline(object):
    def process_item(self, item, spider):
        if "level_subjects" == spider.name:
            print(item)
            return item
        return item


class LibraryChapterPipeLine(object):
    def process_item(self, item, spider):
        if "library_chapter" == spider.name:
            print(item)
            from jyeoo.mysql_model import DBSession, LibraryChapter
            session = DBSession()
            session.add(LibraryChapter(**item))
            return item
        return item
