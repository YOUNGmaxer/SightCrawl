import pymongo
from sights.dbs.mongoBase import MongoBaseClient

class SightsPipeline(object):
  def process_item(self, item, spider):
    return item

class MongoPipeline(object):
  def __init__(self, mongo_host, mongo_port, mongo_db):
    self.mongo_host = mongo_host
    self.mongo_port = mongo_port
    self.mongo_db = mongo_db
    self.mongoClient = MongoBaseClient(self.mongo_host, self.mongo_port, self.mongo_db)

  @classmethod
  def from_crawler(cls, crawler):
    return cls(
      mongo_host = crawler.settings.get('MONGO_HOST'),
      mongo_port = crawler.settings.get('MONGO_PORT'),
      mongo_db = crawler.settings.get('MONGO_DB')
    )

  def open_spider(self, spider):
    # TODO: 这里的 collection 应该存在其他地方
    self.collection = spider.KEYWORD
    self.mongoClient.connectMongo()
    self.mongoClient.setIndex(self.collection, [('sight_id', 1)], unique=True)

  def process_item(self, item, spider):
    self.mongoClient.insertItem(self.collection, dict(item))
    return item

  def close_spider(self, spider):
    self.mongoClient.closeDB()
