# -*- coding: utf-8 -*-
import scrapy

class House(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    houseId = scrapy.Field()
    estateId = scrapy.Field()
    estateLianjiaId = scrapy.Field()
    estateName = scrapy.Field()
    gmtCreated = scrapy.Field()
    houseType = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    time = scrapy.Field()
    price = scrapy.Field()

    Latitude = scrapy.Field()
    city = scrapy.Field()