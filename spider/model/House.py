
import scrapy

class House(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    estateId = scrapy.Field()
    estateLianjiaId = scrapy.Field()
    estateName = scrapy.Field()
    gmtCreated = scrapy.Field()
    community = scrapy.Field()
    model = scrapy.Field()
    area = scrapy.Field()
    focus_num = scrapy.Field()
    watch_num = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()
    average_price = scrapy.Field()

    Latitude = scrapy.Field()
    city = scrapy.Field()