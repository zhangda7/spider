# -*- coding: utf-8 -*-

import requests
from threading import Timer
import time
import logging
import sys, traceback
import spider.Constants as Constants

class ProxyService():
    def __init__(self):
        self.logger = logging.getLogger(ProxyService.__name__)
        self.logger.setLevel(logging.DEBUG)
        # self.proxys = []
        # self.proxyNum = 0

    # def getProxy(self, index):
    #     return self.proxys[index % self.proxyNum]

    def fetchOnce(self):
        self.logger.info("Begin retrive proxys")
        try:
            res = requests.get('http://127.0.0.1:8000')
            self.parseProxyData(res)
        except Exception:
            exc_info = sys.exc_info()
            traceback.print_exception(*exc_info)
            del exc_info

        Timer(300, self.fetchOnce).start()
        pass

    def parseProxyData(self, res):
        array = res.json()
        proxyNew = []
        for one in array:
            self.logger.info(one)
            oneProxy = "http://" + one[0] + ":" + str(one[1])
            self.logger.info("Find one %s", oneProxy)
            proxyNew.append(oneProxy)
        Constants.proxys.clear()
        Constants.proxys.extend(proxyNew)

    def start(self):
        self.fetchOnce()


if __name__ == "__main__":
    # fileConfig('logging_config.ini')
    logging.basicConfig(level=logging.INFO)
    proxy = ProxyService()
    proxy.start()

    time.sleep(10500)




