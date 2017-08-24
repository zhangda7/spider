# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from lxml import etree
import sys
from time import gmtime, strftime
import datetime
from ..model.House import House
from .. import Constants
import traceback
import logging
host = "sh.lianjia.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'
host = "sh.lianjia.com"
accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
acceptEncoding = 'gzip, deflate'
acceptLanguage = 'en,zh-CN;q=0.8,zh;q=0.6'
connection = 'keep-alive'
'''cookie = 'lianjia_uuid=2b4b168c-01e5-4a65-b273-31c4777675a5; sample_traffic_test=test_68; ' \
         'UM_distinctid=15cb17e0a906b-0cb5c330e02bcc-50462f1d-fa000-15cb17e0a919ef; _smt_uid=5943f74e.9aa7704;' \
         ' _gid=GA1.2.1073981028.1497626449; select_city=310000; cityCode=sh; _gat_u=1;' \
         ' gr_user_id=e250af47-e509-43ef-8eee-395c5de3eb42; _gat=1; _ga=GA1.2.1312901874.1497626449;' \
         ' gr_session_id_970bc0baee7301fa=4c1d8940-113a-42b0-86e2-7f62a38daeaa;' \
         ' lianjia_ssid=8580a132-fdb4-440a-8c64-468a7f925626;' \
         ' ubt_load_interval_b=1497627475374; ubt_load_interval_c=1497627475374;' \
         ' ubta=2299869246.390599322.1497627011303.1497627318339.1497627475503.4; ' \
         'ubtb=2299869246.390599322.1497627475504.6B6B25625B89F964C76E30B5314BADCF;' \
         ' ubtc=2299869246.390599322.1497627475504.6B6B25625B89F964C76E30B5314BADCF; ubtd=4'''''
cookie = 'aliyungf_tc=AQAAAEEteSlPCgEANmbJ2vIvFVQ+RQ+Q; Path=/; HttpOnly; ' \
         'select_city=310000; Domain=.lianjia.com; Path=/; ' \
         'cityCode=sh; Domain=.lianjia.com; Path=/;' \
         'lianjia_uuid=117f845b-aec5-473d-9670-1cecab05a3ae; Domain=.lianjia.com; Expires=Thu, 18-Aug-2022 04:49:51 GMT; Path=/ '
headers = {'User-Agent': user_agent, "Accept": accept, "Accept-Encoding": acceptEncoding,
           "Accept-Language": acceptLanguage, "Cookie": cookie, "Connection": connection,
           "Host": host, "Upgrade-Insecure-Requests": 1}

class HouseSpiderV2(scrapy.Spider):
    def __init__(self):
        self.logger.info("HouseSpiderV2 init")
        # self.startUrl = Constants.pending_urls.get(False)
        # if(self.startUrl == None):
        #     self.logger.error("Can not get start url")
        # self.logger = logging.getLogger("HouseSpider")
    name = 'houseSpiderV2'
    # start_urls = 'http://sh.lianjia.com/xiaoqu/5011000018129.html'
    def start_requests(self):
        # self.start_urls = []
        for i in range(Constants.CONCURRENT_REQUEST):
            startUrl = Constants.pending_urls.get(False)
            self.logger.info("Yield request %s", startUrl)
            yield scrapy.Request(url=startUrl, headers=headers, method='GET', callback=self.parseHouseList, dont_filter=True, errback = lambda x: self.downloadErrorBack(x, startUrl))

    def get_latitude(self,url):  # 进入每个房源链接抓经纬度
        p = requests.get(url)
        contents = etree.HTML(p.content.decode('utf-8'))
        latitude = contents.xpath('/ html / body / script[19]/text()').pop()
        time.sleep(5)
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
            self.logger.info("Url %s get response, house size %d", response.url, len(houselist))
            for house in houselist:
                try:
                    item = House()
                    estateLink = house.xpath('div/div[2]/div[2]/span[1]/a[1]/@href').pop()
                    curLianjiaId = self.getLianjiaId(estateLink)
                    curEstate = Constants.estateMap[curLianjiaId]
                    item['title'] = house.xpath('div/div[1]/a/text()').pop()
                    item['link'] = Constants.LIANJIA_HOST + house.xpath('div/div[1]/a/@href').pop()
                    item["houseId"] = self.getHouseLianjiaId(item['link'])
                    item['estateId'] = curEstate["_id"]
                    item["estateLianjiaId"] = curEstate[Constants.LIANJIA_ID]
                    item["estateName"] = curEstate["name"]
                    # item["gmtCreated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    item["gmtCreated"] = datetime.datetime.utcnow()
                    try:
                        item['price'] = float(house.xpath('div/div[2]/div[1]/div/span[1]/text()').pop())
                    except Exception:
                        self.logger.error("ERROR on parse price of %s", item['link'])
                        item['price'] = house.xpath('div/div[2]/div[1]/div/span[1]/text()').pop()
                    # item['price'] = house.xpath('div/div[2]/div[1]/div/span[1]/text()').pop()
                    item['city'] = "Shanghai"
                    #////*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/ul/li[1]/div/div[2]/div[1]/span/text()
                    item['houseType'] = house.xpath('div/div[2]/div[1]/span/text()').pop().split('|')[0].strip()
                    item['area'] = house.xpath('div/div[2]/div[1]/span/text()').pop().split('|')[1].strip()
                    item['floor'] = house.xpath('div/div[2]/div[1]/span/text()').pop().split('|')[2].strip()
                except Exception:
                    exc_info = sys.exc_info()
                    traceback.print_exception(*exc_info)
                    self.logger.error("ERROR on parse houselist of %s", response.url)
                    del exc_info
                    pass
                self.logger.info("Get one house info %s", item["title"])
                yield item
            pageCountList = response.xpath('count(//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/a)').extract()
            #这里需要进行判空操作
            #//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/span
            curPageList = response.xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/span/text()')
            if(curPageList == None or len(curPageList) == 0):
               self.logger.info("Page %s has no curPage, should remove it", response.url)
            else:
                curPageStr = response.xpath('//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/span/text()').extract().pop()
                pageCount = int(float(pageCountList[0]))
                curPage = int(curPageStr)
                if(pageCount == 0 or pageCount <= curPage):
                    self.logger.info("No next page on %s %d %d", curPageStr, curPage, pageCount)
                else:
                    nextPageXPath = '//*[@id="js-ershoufangList"]/div[2]/div[3]/div[1]/div[2]/a[' + str(pageCount) + ']/@href'
                    nextPage = Constants.LIANJIA_HOST + selector.xpath(nextPageXPath).pop()
                    self.logger.info("Find next page : %s", nextPage)
                    self.logger.info("Yield request %s", nextPage)
                    yield scrapy.Request(url=nextPage, headers=headers,
                                         method='GET', callback=self.parseHouseList, errback = lambda x: self.downloadErrorBack(x, nextPage))
        except Exception:
            self.logger.error("Page %s has error", response.url)
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info
            pass
        try:
            if(not Constants.pending_urls.empty()):
                nextUrl = Constants.pending_urls.get(False)
                self.logger.info("Yield request for queue next %s", nextUrl)
                yield scrapy.Request(url=nextUrl, headers=headers,
                                     method='GET', callback=self.parseHouseList, errback = lambda x: self.downloadErrorBack(x, nextUrl))
        except Exception:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info
            pass
    def parseHouseDetail(self,response):
        pass

    def downloadErrorBack(self, e, url):
        self.logger.error("Url %s download error %s", url, e)
        yield scrapy.Request(url=url, headers=headers, method='GET', callback=self.parseHouseList,
                             dont_filter=True, errback = lambda x: self.downloadErrorBack(x, url))
        pass

    def getLianjiaId(self, link):
        i1 = link.rfind("/")
        ret = link[i1 + 1:len(link) - 5]
        return ret

    def getHouseLianjiaId(self, link):
        i1 = link.rfind("/")
        ret = link[i1 + 1:len(link) - 5]
        return ret