# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from  scrapy import Item
class NewsSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


import pymongo
class MongoDBPipeline(object):
    """
    将item写入MongoDB
    """

    @classmethod
    def from_crawler(cls, crawler):
        cls.DB_URL = crawler.settings.get('MONGO_DB_URI', 'mongodb://localhost:27017')
        cls.DB_NAME = crawler.settings.get('MONGO_DB_NAME', 'scrapy_data')
        return cls()

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.DB_URL)
        self.db = self.client[self.DB_NAME]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        if collection.find({'title': dict(item)['title']}).limit(1).count() > 0:
            print('999999')
        else:
            post = dict(item) if isinstance(item, Item) else item
            collection.insert_one(post)
        return item
