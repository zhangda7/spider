# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from lxml import etree
from ..model.Estate import Estate
from time import gmtime, strftime
from spider import Constants
import traceback, sys

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

class EstateListSpider(scrapy.Spider):
    name = 'estateSpider'

    def start_requests(self):
        self.start_urls = "http://sh.lianjia.com/xiaoqu/qingpu/d"
        for i in range(1, 100):
            full_url = self.start_urls + str(i)
            yield scrapy.Request(url=full_url, headers=headers, method='GET', callback=self.parseEstateList, dont_filter=True)
            #time.sleep(10)

    def parseEstateList(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        lists = response.body.decode('utf-8')
        selector = etree.HTML(lists)

        estatelist = selector.xpath('//*[@id="house-lst"]/li')
        for estateHtml in estatelist:
            try:
                # print("Result:" + lists)
                estate = Estate()
                estate["name"] = estateHtml.xpath('div[2]/h2/a/text()').pop()
                estate["link"] = Constants.LIANJIA_HOST + estateHtml.xpath('div[2]/h2/a/@href').pop()
                estate["district"] = estateHtml.xpath("div[2]/div[1]/div[2]/div/a[1]/text()").pop()
                estate["gmtCreated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                estate[Constants.LIANJIA_ID] = self.getLianjiaId(estate["link"])

                self.logger.info("Estate %s %s", estate["name"], estate["link"])
                yield estate
            except Exception:
                exc_info = sys.exc_info()
                traceback.print_exception(*exc_info)
                del exc_info
        #handle next page

    def getLianjiaId(self, link):
        i1 = link.rfind("/")
        ret = link[i1 + 1:len(link) - 5]
        return ret