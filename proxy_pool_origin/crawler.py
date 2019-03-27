import json
from pyquery import PyQuery as pq
from utils import PageGetter
from lxml import etree

# 此为元类(metaclass)，必须从 type 类型派生
class ProxyMetaclass(type):
  def __new__(cls, name, bases, attrs):
    count = 0
    attrs['__CrawlFunc__'] = []
    # key, value, 会遍历类的方法，然后发现有 crawl_ 前缀的就加到一个字典里面
    for k, v in attrs.items():
      if 'crawl_' in k:
        attrs['__CrawlFunc__'].append(k)
        count += 1
    attrs['__CrawlFuncCount__'] = count
    return type.__new__(cls, name, bases, attrs)
    
class Crawler(object, metaclass=ProxyMetaclass):
  def get_proxies(self, callback):
    proxies = []
    # eval 执行一个字符串，并返回结果
    # 此处为返回爬取到的可用·代理
    for proxy in eval('self.{}()'.format(callback)):
      print('成功获取到代理', proxy)
      proxies.append(proxy)
    return proxies
  
  def crawl_daili66(self, page_count=8):
    '''
    获取代理，来源为66ip
    :param page_count: 页码
    :return: 代理
    '''
    print('开始获取 66ip 的代理')
    start_url = 'http://www.66ip.cn/{}.html'
    # 利用列表推导式获取网页地址的列表
    urls = [start_url.format(page) for page in range(1, page_count + 1)]
    for url in urls:
      print('Crawling', url)
      html = PageGetter().get_page(url)
      if html:
        doc = etree.HTML(html)
        trs = doc.xpath('//div[contains(@class, "containerbox")]//table//tr[position()>1]')
        for tr in trs:
          tds = tr.getchildren()
          ip = tds[0].text
          port = tds[1].text
          # print('[ip, port]', ip, port)
          yield ':'.join([ip, port])
