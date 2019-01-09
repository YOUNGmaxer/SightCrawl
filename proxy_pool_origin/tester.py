'''
@Description: In User Settings Edit
@Author: YOUNG
@Date: 2019-01-04 13:43:34
@LastEditTime: 2019-01-07 19:53:02
@LastEditors: Please set LastEditors
'''
from redisClient import RedisClient
import aiohttp
import asyncio

VALID_STATUS_CODES = [200]
# 此测试链接最好设置为有抓取需求的网站
TEST_URL = 'http://www.baidu.com'
BATCH_TEST_SIZE = 100

class Tester(object):
  def __init__(self):
    self.redis = RedisClient()

  async def test_single_proxy(self, proxy):
    '''
    测试单个代理
    :param proxy: 单个代理
    :return: None
    '''
    conn = aiohttp.TCPConnector(verify_ssl=False)
    # 添加 async 表明是异步方法
    async with aiohttp.ClientSession(connector=conn) as session:
      try:
        if isinstance(proxy, bytes):
          proxy = proxy.decode('utf-8')
        real_proxy = 'http://' + proxy
        print('正在测试', proxy)
        # 添加 async 表明是异步请求
        async with session.get(TEST_URL, proxy=real_proxy, timeout=15) as response:
          # 检查响应状态是否为 200
          if response.status in VALID_STATUS_CODES:
            self.redis.max(proxy)
          else:
            self.redis.decrease(proxy)
            # print('请求响应码不合法', proxy)
      except (TimeoutError, AttributeError):
        self.redis.decrease(proxy)
        print('代理请求失败', proxy)

  def run(self):
    '''
    测试主函数
    :return: None
    '''
    print('测试器开始运行')
    try:
      proxies = self.redis.all()
      loop = asyncio.get_event_loop()
      # 批量测试
      for i in range(0, len(proxies), BATCH_TEST_SIZE):
        test_proxies = proxies[i:i + BATCH_TEST_SIZE]
        tasks = [self.test_single_proxy(proxy) for proxy in test_proxies]
        loop.run_until_complete(asyncio.wait(tasks))
    except Exception as e:
      print('测试器发生错误', e.args)