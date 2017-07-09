from spider.spiders.EstateListSpider import EstateListSpider
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

def startCrawler():
    RUNNING_CRAWLERS.append(1)
    crawler = Crawler(EstateListSpider, settings)
    # stop reactor when spider closes
    crawler.signals.connect(spider_closing, signal=signals.spider_closed)

    crawler.crawl()

    reactor.run()

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO
    )
    Constants.FLAG = 2
    startCrawler()