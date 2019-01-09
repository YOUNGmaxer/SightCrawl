import scrapy
import os
import requests
import base64
import json
from PIL import Image
from scrapy.shell import inspect_response
from scrapy.loader import ItemLoader
from sights.items import SightsItem
from sights.utils import baidu_ocr

class HotSightSpider(scrapy.Spider):
  name = 'qunar-hot-sights'
  page_num = 1
  KEYWORD = '热门景点'
  proxy = None
  # BAIDU_OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate?access_token=24.b190c799dc1d8a9c48d276a9cd92d084.2592000.1549069278.282335-15327006'

  start_urls = [
    'http://piao.qunar.com/ticket/list.htm?keyword=' + KEYWORD
  ]

  def parse(self, response):
    '''
    用于分析和提取去哪儿网的页面内容
    @url http://piao.qunar.com/ticket/list.htm?keyword=深圳
    @returns items
    @scrapes sight_name sight_id sight_districts sight_point sight_address sight_sale_count
    '''
    print('状态', response.status)
    page_list = response.xpath('//div[@class="result_list"]/div[contains(@class, "sight_item")]')
    page_len = len(page_list)
    for page_item in page_list:
      # l = ItemLoader(item=SightsItem(), response=response)
      # l.add_css('sight_name', 'div.sight_item::attr({})'.format('data-sight-name'))
      # l.add_css('sight_id', 'div.sight_item::attr({})'.format('data-id'))
      # l.add_css('sight_districts', 'div.sight_item::attr({})'.format('data-districts'))
      # l.add_css('sight_point', 'div.sight_item::attr({})'.format('data-point'))
      # l.add_css('sight_address', 'div.sight_item::attr({})'.format('data-address'))
      # l.add_css('sight_sale_count', 'div.sight_item::attr({})'.format('data-sale-count'))
      # yield l.load_item()

      item = SightsItem()
      item['sight_name'] = self.parse_page_item(page_item, 'data-sight-name')
      item['sight_id'] = self.parse_page_item(page_item, 'data-id')
      item['sight_districts'] = self.parse_page_item(page_item, 'data-districts')
      item['sight_point'] = self.parse_page_item(page_item, 'data-point').split(',')
      item['sight_address'] = self.parse_page_item(page_item, 'data-address')
      item['sight_sale_count'] = self.parse_page_item(page_item, 'data-sale-count')
      yield item
    
    # 自动爬取下一页
    if page_len > 0:
      self.page_num += 1
      next_url = self.start_urls[0] + '&page={}'.format(self.page_num)
      print('正在爬取第 {} 页的数据'.format(self.page_num))
      yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)
    else:
      robot_page = response.xpath('//div[@class="mp-robot-formcon"]')
      if robot_page is not None:
        print('爬虫被中断: 可能IP被封')
        print(robot_page)
      #   robot_img_url = response.xpath('//div[@class="mp-robot-formcon"]//img[@class="mp-captchaimg"]/@src').extract_first()
      #   yield scrapy.Request(robot_img_url, callback=self.parse_robot_img)

  def parse_page_item(self, page_item, data_info):
    return page_item.css('div.sight_item::attr(%s)' % data_info).extract_first()

  # 分析反爬虫验证码并破解
  def parse_robot_img(self, response):
    print(response.status)
    if response.status == 200:
      file_path = 'sights/images/{0}.{1}'.format(self.KEYWORD, 'jpg')
      # 将验证码图片下载下来
      with open(file_path, 'wb') as f:
        f.write(response.body)
      ocr_res = baidu_ocr.transImage2Text(file_path)
      print('ocr_res', ocr_res)
      
