import redis
from random import choice
import scrapy
import logging

logger = logging.getLogger(__name__)

MAX_SCORE = 20
MIN_SCORE = 0
INITIAL_SCORE = 10
REDIS_HOST = '106.13.70.140'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_KEY = 'proxies'

class RedisClient(object):
  def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
    '''
    初始化
    :param host: Redis 地址
    :param port: Redis 端口
    :param password: Redis 密码
    '''
    try:
      ret = self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)
      print('连接数据库成功！', ret)
    except Exception as e:
      print('连接数据库异常！', e)

  def add(self, proxy, score=INITIAL_SCORE, key=REDIS_KEY):
    '''
    添加代理，设置分数
    :param proxy: 代理
    :param score: 分数
    :return: 添加结果
    '''
    try:
      if not self.db.zscore(key, proxy):
        # 向键名为 'REDIS_KEY' 的添加 score 和 proxy
        return self.db.zadd(key, {proxy: score})
    except redis.exceptions.ConnectionError as e:
      logger.error('连接异常 %r', e)

  
  def random(self):
    '''
    随机获取有效代理，首先尝试获取最高分数代理，如果最高分数不存在，则按照排名获取，否则异常
    :return: 随机代理
    '''
    # 返回 min ～ max 之间的键值。这里想返回最高分。
    result = self.db.zrangebyscore(REDIS_KEY, min=MAX_SCORE, max=MAX_SCORE)
    if len(result):
      return choice(result)
    else:
      # 按排名选取前100
      result = self.db.zrevrange(REDIS_KEY, 0, 100)
      if len(result):
        # 返回列表中随机一项
        return choice(result)
      else:
        # raise PoolEmptyError
        print('PoolEmptyError')
    
  def decrease(self, proxy):
    '''
    代理值减一分，分数小于最小值，则代理删除
    :param proxy: 代理
    :return: 修改后的代理分数
    '''
    # 获取某个代理的分数
    score = self.db.zscore(REDIS_KEY, proxy)
    if score and score > MIN_SCORE:
      print('代理', proxy, '不可用，当前分数', score, '减1')
      # 修改 proxy 的分数
      incrby_res =  self.db.zincrby(REDIS_KEY, -1, proxy)
      if incrby_res:
        print('[修改] 修改分数成功！代理 {0} 当前分数: {1}'.format(proxy, incrby_res))
      else:
        print('[修改] 修改分数失败！')
    else:
      print('代理', proxy, '当前分数', score, '移除')
      # 删除 proxy
      rem_res = self.db.zrem(REDIS_KEY, proxy)
      if rem_res:
        print('[删除] 删除代理 {} 成功！'.format(proxy))
      else:
        print('[删除] 删除代理 {} 失败！'.format(proxy))

  def exists(self, proxy, key=REDIS_KEY):
    '''
    判断代理是否存在
    :param proxy: 代理
    :return: 是否存在
    '''
    return not self.db.zscore(key, proxy) == None

  def max(self, proxy):
    '''
    将代理设置为 MAX_SCORE
    :param proxy: 代理
    :return: 设置结果
    '''
    print('代理', proxy, '可用，设置为', MAX_SCORE)
    return self.db.zadd(REDIS_KEY, {proxy: MAX_SCORE})

  def count(self, key=REDIS_KEY):
    '''
    获取数量
    :return: 数量
    '''
    # 返回该有序集合的元素的个数
    return self.db.zcard(key)

  def all(self):
    '''
    获取全部代理
    :return: 全部代理列表
    '''
    return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
