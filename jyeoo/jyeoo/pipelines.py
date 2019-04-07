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


class ItemBankPipeLine(object):
    def process_item(self, item, spider):
        if "item_bank" == spider.name:
            from jyeoo.mysql_model import DBSession, ItemBank, ChaperPoint, ItemPoint
            session = DBSession()
            item_dict = dict(**item)
            point_list = item_dict.pop('point')

            for point in point_list:
                chaper_point = dict()
                chaper_point['chaper_id'] = point.get('chaper_id')
                chaper_point['title'] = ''  # point.get('url')
                chaper_point['code'] = point.get('point_code')
                chaper_point['content'] = point.get('url')
                session.add(ChaperPoint(**chaper_point))
                item_point = dict()
                item_point['item_id'] = point.get('item_id')
                item_point['point_code'] = point.get('point_code')
                session.add(ItemPoint(**item_point))
            print(item_dict)
            session.add(ItemBank(**item_dict))
            return item
        return item
