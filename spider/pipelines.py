# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.conf import settings

from .items import LianjiaItem
from .model.Estate import Estate
from .model.House import House
from spider import Constants

import sys
class SpiderPipeline(object):
    def __init__(self):
        host = "127.0.0.1"
        port = 27017
        db_name = "lianjia"
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.estateCollection = tdb["estate.detail"]
        self.houseCollection = tdb["house.detail"]
        self.estateAllCollection = tdb["estate.all"]

    def process_item(self, item, spider):
        if Constants.FLAG == 2:
            self.handleEstateAll(item)
            return item
        if isinstance(item, Estate):
            try:
                info = dict(item)
                if self.estateCollection.insert(info):
                    print('bingo')
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                pass
        elif isinstance(item, House):
            try:
                info = dict(item)
                if self.houseCollection.insert(info):
                    print('bingo')
            except Exception:
                print("Unexpected error:", sys.exc_info()[0])
                pass
        return item

    def handleEstateAll(self, item):
        try:
            info = dict(item)
            if(self.estateAllCollection.count({Constants.LIANJIA_ID:item[Constants.LIANJIA_ID]}) == 0):
                if self.estateAllCollection.insert(info):
                    print('bingo')
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            pass