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

from w3lib.url import safe_url_string
from six.moves.urllib.parse import urljoin
from scrapy.downloadermiddlewares.redirect import BaseRedirectMiddleware

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
        proxy = random.choice(Constants.proxys)
        request.meta['proxy'] = proxy
        self.logger.warning("Current proxy : %s", request.meta['proxy'])

logger = logging.getLogger(__name__)

class CheckRedirect(BaseRedirectMiddleware):
    # def __init__(self):
    #     self.logger = logging.getLogger(CheckRedirect.__name__)

    def process_response(self, request, response, spider):
        if (request.meta.get('dont_redirect', False) or
                response.status in getattr(spider, 'handle_httpstatus_list', []) or
                response.status in request.meta.get('handle_httpstatus_list', []) or
                request.meta.get('handle_httpstatus_all', False)):
            return response

        allowed_status = (301, 302, 303, 307)
        if 'Location' not in response.headers or response.status not in allowed_status:
            return response

        location = safe_url_string(response.headers['location'])

        redirected_url = urljoin(request.url, location)


        if(redirected_url == request.url):
            logger.info("Url %s %s, equal", redirected_url, request.url)
            #must return response to pass to next middleware
            # return response
            pass
        else:
            logger.info("Url %s %s, not equal, just retry request from scratch", redirected_url, request.url)
            #set redirect url
            redirected_url = request.url
            return request

        if response.status in (301, 307) or request.method == 'HEAD':
            redirected = request.replace(url=redirected_url)
            return self._redirect(redirected, request, spider, response.status)

        redirected = self._redirect_request_using_get(request, redirected_url)
        return self._redirect(redirected, request, spider, response.status)

        # if response.status in (301, 307) or request.method == 'HEAD':
        #     redirected = request.replace(url=redirected_url)
        #     return self._redirect(redirected, request, spider, response.status)
        #
        # redirected = self._redirect_request_using_get(request, redirected_url)
        # return self._redirect(redirected, request, spider, response.status)

class CatchExceptionMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(CatchExceptionMiddleware.__name__)

    def process_response(self, request, response, spider):
        if response.status < 200 or response.status >= 400:
            try:
                yield scrapy.Request(url=request, headers=headers, method='GET', callback=self.parseHouseList, dont_filter=True)
                self.logger.warning("Proxy %s fail", request.meta['proxy'])
                Constants.failedProxys.append(request.meta['proxy'])
                Constants.proxys.remove(request.meta['proxy'])
            except KeyError:
                pass
        return response

    def process_exception(self, request, exception, spider):
        try:
            Constants.failedProxys.append(request.meta['proxy'])
            Constants.proxys.remove(request.meta['proxy'])
        except Exception:
            pass