# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from lxml import etree
from ..items import LianjiaItem
from ..model.Estate import Estate
#from scrapy_redis.spiders import RedisSpider

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

class EstateSpider(scrapy.Spider):
    name = 'estateSpider'
    start_urls = 'http://sh.lianjia.com/xiaoqu/5011000018129.html'
    def start_requests(self):

        yield scrapy.Request(url=self.start_urls, headers=headers, method='GET', callback=self.parseEstate, dont_filter=True)

    def parseEstate(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)
        #print("Result:" + lists)
        estate = Estate()
        estate["name"] = selector.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/h1/text()').pop()
        estate["address"] = selector.xpath('/html/body/div[4]/div[1]/section/div[1]/div[1]/span/span[2]/text()').pop()
        estate["district"] = selector.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[6]/span/a/text()').pop()
        estate["year"] = selector.xpath('//*[@id="zoneView"]/div[2]/div[3]/ol/li[2]/span/span/text()').pop()
        estate["average_price"] = selector.xpath('//*[@id="zoneView"]/div[2]/div[2]/div/p[2]/span[1]/text()').pop()
        estate["houseLink"] = host + selector.xpath('//*[@id="res-nav"]/ul/li[3]/a/@href').pop()

        self.logger.info("House %s %s %s %s %s", estate["name"], estate["address"],
                         estate["district"], estate["year"], estate["average_price"], estate["houseLink"])
        yield estate