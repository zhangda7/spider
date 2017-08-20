from spider.spiders.HouseSpiderV2 import HouseSpiderV2
import logging
import pymongo
from spider import Constants
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.util import ProxyService
from scrapy.utils.log import configure_logging

RUNNING_CRAWLERS = []

def startCrawler(startEstates):
    for startEstate in startEstates:
        Constants.estateMap[startEstate[Constants.LIANJIA_ID]] = startEstate
        Constants.pending_urls.put(startEstate["houseLink"])

    print("Total estate num :" + str(Constants.pending_urls.qsize()))
    crawler = CrawlerProcess(get_project_settings())
    crawler.crawl(HouseSpiderV2)

    crawler.start()

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
    configure_logging(install_root_handler=False)
    FORMAT = "%(asctime)s [%(levelname)s] %(threadName)s - %(name)s:%(lineno)d - %(message)s"

    fileHandler = logging.FileHandler('houseJoblog.log', 'w', 'utf-8')  # or whatever
    fileHandler.setFormatter(logging.Formatter(FORMAT))
    logging.getLogger().addHandler(fileHandler)
    logging.basicConfig(
        # filename='houseJoblog.txt',
        format=FORMAT,
        level=logging.INFO
    )
    proxyService = ProxyService.ProxyService()
    proxyService.start()
    startEstates = fetchStartUrls(-1)
    startCrawler(startEstates)