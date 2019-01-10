from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from sights.items import SightsDetailItem
from sights.items import SightsItem
from sights.custom_settings import common_spider_settings

class SightDetailSpider(CrawlSpider):
  name = 'qunar-detail'
  keyword = '普宁'
  proxy = None
  start_urls = [ f'http://piao.qunar.com/ticket/list.htm?keyword={keyword}' ]
  custom_settings = common_spider_settings.settings

  rules = (
    Rule(
      LinkExtractor(restrict_xpaths='//div[@class="sight_item_about"]//a[@class="name"]',),
      callback='parse_item'
    ),
    Rule(
      LinkExtractor(restrict_xpaths='//div[@class="pager"]/a[@class="next"]'),
      follow=True
    )
  )

  def parse_item(self, response):
    item = SightsDetailItem()
    item['name'] = response.xpath('//div[@class="mp-description-detail"]//span[@class="mp-description-name"]/text()').extract_first()
    yield item

  # [重写] 处理 start_urls 返回 response
  def parse_start_url(self, response):
    # 获取景点列表
    page_list = response.xpath('//div[@class="result_list"]/div[contains(@class, "sight_item")]')
    for page_item in page_list:
      item = SightsDetailItem()
      item['name'] = self.extract_item(page_item, 'data-sight-name')
      item['sid'] = self.extract_item(page_item, 'data-id')
      item['districts'] = self.extract_item(page_item, 'data-districts')
      item['point'] = self.extract_item(page_item, 'data-point').split(',')
      item['address'] = self.extract_item(page_item, 'data-address')
      item['sale_count'] = self.extract_item(page_item, 'data-sale-count')
      yield item

  def extract_item(self, page_item, data_info):
    return page_item.css(f'div.sight_item::attr({data_info})').extract_first()
