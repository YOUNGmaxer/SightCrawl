settings = {
  'SETTING_NAME': 'qunar_detail_spider.qunar-detail',
  'DOWNLOADER_MIDDLEWARES': {
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'sights.downloader_middlewares.RandomUserAgentMiddleware': 500,
    'scrapy.downloadermiddlewares.redirect.RedirectMiddleware': None,
    'sights.downloader_middlewares.LocalRedirectMiddleware': 600,
    'sights.downloader_middlewares.ProxyMiddleware': 800,
  },
  'ITEM_PIPELINES': {
    'sights.pipelines.SightsPipeline': 300
  }
}
