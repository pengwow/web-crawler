# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JyeooPipeline(object):
    def process_item(self, item, spider):
        if "level_subjects" == spider.name:
            print(item)
        else:
            return item
        return item
