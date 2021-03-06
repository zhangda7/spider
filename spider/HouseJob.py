from spider.spiders.HouseSpider import HouseSpider
# scrapy api
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.conf import settings
import logging
import pymongo
from spider import Constants
from spider.util import ProxyService

RUNNING_CRAWLERS = []

def spider_closing(spider):
    """Activates on spider closed signal"""
    print("Spider closed: %s" % spider)
    RUNNING_CRAWLERS.pop()
    if not RUNNING_CRAWLERS:
        reactor.stop()
    # if(len(RUNNING_CRAWLERS) == 0):
    #     reactor.stop()

def startCrawler(startEstates):
    # mySettings = Settings()
    # mySettings.set("ITEM_PIPELINES", settings["ITEM_PIPELINES"])
    # settings.set("ITEM_PIPELINES", )
    # settings.set("USER_AGENT",
    #              "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
    crawler = Crawler(HouseSpider, settings)
    RUNNING_CRAWLERS.append(1)
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    for startEstate in startEstates:
        # crawl responsibly
        # houseSpider = HouseSpider(None)
        # houseSpider.startEstate = startEstate
        Constants.estateMap[startEstate[Constants.LIANJIA_ID]] = startEstate
        Constants.pending_urls.put(startEstate["houseLink"])
        # stop reactor when spider closes

        # crawler.configure()

    crawler.crawl(Constants.pending_urls.get(False))
        # crawler.
        # crawler.start()

    reactor.run()

def fetchStartUrls(count):
    host = "127.0.0.1"
    port = 27017
    db_name = "lianjia"
    client = pymongo.MongoClient(host=host, port=port)
    tdb = client[db_name]
    estateCollection = tdb["estate.detail"]
    estates = estateCollection.find()
    startEstates = []
    index = 0
    for estate in estates:
        print(estate["name"], estate["houseLink"])
        startEstates.append(estate)
        index = index + 1
        if(count > 0 and index >= count):
            break
    return startEstates

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )
    # proxyService = ProxyService.ProxyService()
    # proxyService.start()
    startEstates = fetchStartUrls(-1)
    startCrawler(startEstates)