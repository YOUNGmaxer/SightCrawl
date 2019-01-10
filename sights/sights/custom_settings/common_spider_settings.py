settings = {
  'SETTING_NAME': 'common_spider.qunar-detail',
  'DOWNLOADER_MIDDLEWARES': {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None
  },
  'ITEM_PIPELINES': {
    'sights.pipelines.SightsPipeline': 300
  }
}
