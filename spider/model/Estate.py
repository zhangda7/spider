# -*- coding: utf-8 -*-
import scrapy

class Estate(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    address = scrapy.Field()
    district = scrapy.Field()
    year = scrapy.Field()
    average_price = scrapy.Field()
    houseLink = scrapy.Field()
    gmtCreated = scrapy.Field()
    lianjiaId = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    #标识入库方式
    flag = scrapy.Field()