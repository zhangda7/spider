# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import logging
import random
import spider.Constants as Constants
from scrapy import signals
import scrapy


class SpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class ProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(ProxyMiddleware.__name__)

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        if(len(Constants.proxys)== 0):
            return
        proxy = random.choice(Constants.proxys)
        request.meta['proxy'] = proxy
        self.logger.warning("Current proxy : %s for request %s", request.meta['proxy'], request.url)

class CatchExceptionMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(CatchExceptionMiddleware.__name__)

    def process_response(self, request, response, spider):
        #看起来，返回request就是retry，返回response就不retry
        self.logger.warning("Request %s Proxy %s status %d", request.url, request.meta['proxy'], response.status)
        if response.status != 200:
            try:
                # yield scrapy.Request(url=request, headers=headers, method='GET', callback=self.parseHouseList, dont_filter=True)
                # self.logger.warning("Proxy %s fail", request.meta['proxy'])
                Constants.failedProxys.append(request.meta['proxy'])
                Constants.proxys.remove(request.meta['proxy'])
                return request
            except KeyError:
                pass
        return response

    def process_exception(self, request, exception, spider):
        try:
            Constants.failedProxys.append(request.meta['proxy'])
            Constants.proxys.remove(request.meta['proxy'])
            # return request
        except Exception:
            pass
        return request