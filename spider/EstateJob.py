from spider.spiders.EstateSpider import EstateSpider
# scrapy api
from scrapy import signals
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy.conf import settings
import logging
import pymongo
from spider import Constants

RUNNING_CRAWLERS = []
logger = logging.getLogger()
def spider_closing(spider):
    """Activates on spider closed signal"""
    logger.info("Spider closed: %s" % spider)
    RUNNING_CRAWLERS.pop()
    if not RUNNING_CRAWLERS:
        reactor.stop()
    # if(len(RUNNING_CRAWLERS) == 0):
    #     reactor.stop()

def startCrawler(startEstates):
    RUNNING_CRAWLERS.append(1)
    crawler = Crawler(EstateSpider, settings)
    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)
    for startEstate in startEstates:
        # crawl responsibly
        Constants.pending_urls.put(startEstate["url"])

    crawler.crawl(Constants.pending_urls.get(False))

    reactor.run()

def scanMissedEstate():
    host = "127.0.0.1"
    port = 27017
    db_name = "lianjia"
    client = pymongo.MongoClient(host=host, port=port)
    tdb = client[db_name]
    estateCollection = tdb["estate.detail"]
    estateTraceCol = tdb["estate.trace"]
    estates = estateCollection.find()
    traces = estateTraceCol.find()
    toAddEstates = []
    curEstates = dict()
    for one in estates:
        curEstates[one[Constants.LIANJIA_ID]] = one

    for one in traces:
        if(not one[Constants.LIANJIA_ID] in curEstates):
            toAddEstates.append(one)

    return toAddEstates

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )
    startEstates = scanMissedEstate()
    if(len(startEstates) == 0):
        logger.info("Estate count is OK. Just stop.")
    else:
        startCrawler(startEstates)