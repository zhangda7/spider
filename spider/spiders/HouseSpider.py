# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from lxml import etree
import sys
from time import gmtime, strftime
from ..model.House import House
#from scrapy_redis.spiders import RedisSpider
import logging
host = "sh.lianjia.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
host = "sh.lianjia.com"
accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
acceptEncoding = 'gzip, deflate'
acceptLanguage = 'en,zh-CN;q=0.8,zh;q=0.6'
connection = 'keep-alive'
cookie = 'lianjia_uuid=2b4b168c-01e5-4a65-b273-31c4777675a5; sample_traffic_test=test_68; ' \
         'UM_distinctid=15cb17e0a906b-0cb5c330e02bcc-50462f1d-fa000-15cb17e0a919ef; _smt_uid=5943f74e.9aa7704;' \
         ' _gid=GA1.2.1073981028.1497626449; select_city=310000; cityCode=sh; _gat_u=1;' \
         ' gr_user_id=e250af47-e509-43ef-8eee-395c5de3eb42; _gat=1; _ga=GA1.2.1312901874.1497626449;' \
         ' gr_session_id_970bc0baee7301fa=4c1d8940-113a-42b0-86e2-7f62a38daeaa;' \
         ' lianjia_ssid=8580a132-fdb4-440a-8c64-468a7f925626;' \
         ' ubt_load_interval_b=1497627475374; ubt_load_interval_c=1497627475374;' \
         ' ubta=2299869246.390599322.1497627011303.1497627318339.1497627475503.4; ' \
         'ubtb=2299869246.390599322.1497627475504.6B6B25625B89F964C76E30B5314BADCF;' \
         ' ubtc=2299869246.390599322.1497627475504.6B6B25625B89F964C76E30B5314BADCF; ubtd=4'
headers = {'User-Agent': user_agent, "Accept": accept, "Accept-Encoding": acceptEncoding,
           "Accept-Language": acceptLanguage, "Cookie": cookie, "Connection": connection,
           "Host": host, "Upgrade-Insecure-Requests": 1}

class HouseSpider(scrapy.Spider):
    def __init__(self, startEstate):
        self.startEstate = startEstate
        # self.logger = logging.getLogger("HouseSpider")
    name = 'houseSpider'
    # start_urls = 'http://sh.lianjia.com/xiaoqu/5011000018129.html'
    def start_requests(self):
        # self.start_urls = []
        self.start_urls = self.startEstate["houseLink"]
        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parseHouseList, dont_filter=True)

    def get_latitude(self,url):  # 进入每个房源链接抓经纬度
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        latitude = contents.xpath('/ html / body / script[19]/text()').pop()
        time.sleep(3)
        regex = '''resblockPosition(.+)'''
        items = re.search(regex, latitude)
        content = items.group()[:-1]  # 经纬度
        longitude_latitude = content.split(':')[1]
        return longitude_latitude[1:-1]

    def parseHouseList(self, response):
        'http://bj.lianjia.com/ershoufang/dongcheng/pg2/'
        time.sleep(2)
        try:
            lists = response.body.decode('utf-8')
            selector = etree.HTML(lists)

            houselist = selector.xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/ul/li')
            for house in houselist:
                try:
                    item = House()
                    item['title'] = house.xpath('div/div[1]/a/text()').pop()
                    item['link'] = house.xpath('div/div[1]/a/@href').pop()
                    item['estateId'] = self.startEstate["_id"]
                    # item["estateLianjiaId"] = self.startEstate["lianjiaId"]
                    item["estateName"] = self.startEstate["name"]
                    item["gmtCreated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    # item['model'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[1]
                    # item['area'] = house.xpath('div[1]/div[2]/div/text()').pop().split('|')[2]
                    # item['focus_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[0]
                    # item['watch_num'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[1]
                    # item['time'] = house.xpath('div[1]/div[4]/text()').pop().split('/')[2]
                    item['price'] = house.xpath('div/div[2]/div[1]/div/span[1]/text()').pop()
                    item['city'] = "Shanghai"
                    #item['Latitude'] = self.get_latitude(self.url_detail)
                except Exception:
                    print("Unexpected error:", sys.exc_info()[0])
                    pass
                self.logger.info("Get one house info %s", item["title"])
                yield item
        except Exception:
            print("Unexpected error:", sys.exc_info()[0])
            pass

    def parseHouseDetail(self,response):
        pass