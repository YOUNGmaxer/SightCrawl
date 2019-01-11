from redisClient import RedisClient
from twisted.trial import unittest
from twisted.internet import defer

class TestRedisClient(unittest.TestCase):
  REDIS_KEY = 'test'

  def setUp(self):
    self.client = RedisClient()
    
  def test_add(self):
    proxy = '127.0.0.1'
    ret = self.client.add(proxy, key=self.REDIS_KEY)
    print('ret', ret)

  def test_exists(self):
    proxy = '127.0.0.1'
    ret = self.client.exists(proxy, key=self.REDIS_KEY)
    print('ret', ret)

  def test_count(self):
    ret = self.client.count(key=self.REDIS_KEY)
    print('ret', ret)
