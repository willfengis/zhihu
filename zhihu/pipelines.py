# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class ZhihuPipeline(object):
    def __init__(self,Mongo_Server,Mongo_DB):
        self.mongo_server = Mongo_Server
        self.mongo_db = Mongo_DB

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            Mongo_Server = crawler.settings.get('MONGO_SERVER'),
            Mongo_DB = crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_server)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db['zhihuuser'].update({'url_token':item['url_token']},{'$set':item},True)
        return item