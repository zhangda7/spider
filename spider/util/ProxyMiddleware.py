#!usr/bin/env
# -*-coding:utf-8 -*-

import logging
import random
import spider.Constants as Constants

#Unused, use middlewares.py instread
class ProxyMiddleware(object):
    def __init__(self):
        self.logger = logging.getLogger(ProxyMiddleware.__name__)

    # overwrite process request
    def process_request(self, request, spider):
        # Set the location of the proxy
        proxy = random.choice(Constants.proxys)
        request.meta['proxy'] = proxy
        self.logger.warning("Current proxy : %s", request.meta['proxy'])
