import scrapy

class SightsItem(scrapy.Item):
    sight_name = scrapy.Field()
    sight_id = scrapy.Field()
    sight_point = scrapy.Field()
    sight_districts = scrapy.Field()
    sight_address = scrapy.Field()
    sight_sale_count = scrapy.Field()
