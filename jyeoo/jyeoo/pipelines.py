# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jyeoo.mysql_model import DBSession, LibraryChapter, ItemBank, ChaperPoint, ItemPoint


class JyeooPipeline(object):
    def process_item(self, item, spider):
        if "level_subjects" == spider.name:
            print(item)
            return item
        return item


class LibraryChapterPipeLine(object):
    session = DBSession()

    def process_item(self, item, spider):
        if "library_chapter" == spider.name:
            print(item)
            self.session.add(LibraryChapter(**item))
            return item
        return item


class ItemBankPipeLine(object):
    session = DBSession()

    def process_item(self, item, spider):
        if "item_bank" == spider.name:
            item_dict = dict(**item)
            point_list = item_dict.pop('point')

            for point in point_list:
                chaper_point = dict()
                chaper_point['chaper_id'] = point.get('chaper_id')
                chaper_point['title'] = point.get('title')  # point.get('url')
                chaper_point['code'] = point.get('point_code')
                chaper_point['url'] = point.get('url')
                self.session.add(ChaperPoint(**chaper_point))
                item_point = dict()
                item_point['item_id'] = point.get('item_id')
                item_point['point_code'] = point.get('point_code')
                self.session.add(ItemPoint(**item_point))
            try:
                self.session.add(ItemBank(**item_dict))
            except Exception as e:
                print(e)
            return item
        return item


class ChapterPointPipeLine(object):
    session = DBSession()

    def process_item(self, item, spider):
        if "chapter_point" == spider.name:
            query = self.session.session.query(ChaperPoint).filter(ChaperPoint.id == item.get('id')).one()
            query.content = item.get('content')
            query.commit()
            return item
        return item
