# -*- coding: utf-8 -*-

import pymongo
import re

from spider.model import Estate

class Service():
    def __init__(self):
        host = "127.0.0.1"
        port = 27017
        db_name = "lianjia"
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.estateAllCollection = tdb["estate.all"]
        self.estateTrace = tdb["estate.trace"]

    def addEstate(self, name, needInsert=True):
        regx = re.compile(".*" + name + ".*", re.IGNORECASE)
        results = self.estateAllCollection.find({"name":regx})
        print(results.count())
        count = 0
        for result in results:
            print("find ", result)
            traceCount = self.estateTrace.count({"lianjiaId":result["lianjiaId"]})
            if(traceCount == 0):
                count = count + 1
                if(needInsert):
                    print("insert to trace")
                    estate = dict()
                    estate["lianjiaId"] = result["lianjiaId"]
                    estate["url"] = result["link"]
                    estate["name"] = result["name"]
                    self.estateTrace.insert(estate)
            else:
                print("Trace already have, no need to insert")
        print("Total need insert count ", count)

if __name__ == "__main__":
    service = Service()
    service.addEstate("苑", False)