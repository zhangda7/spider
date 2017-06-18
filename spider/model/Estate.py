
import scrapy

class Estate(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    year = scrapy.Field()
    average_price = scrapy.Field()
    houseLink = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()