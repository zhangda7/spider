
from time import gmtime, strftime
import datetime

def testGetId():
    str = "http://sh.lianjia.com/xiaoqu/5011000014058.html"
    i1 = str.rfind("/")
    print(i1, len(str) - 5)
    print(str[i1 + 1:len(str) - 5])
    pass

def testList():
    ll = []
    if(ll != None and len(ll) > 0):
        ll.pop()

def testTime():
    obj = datetime.datetime.utcnow();
    print(datetime.datetime.utcnow())

def testHouseId():
    link = "http://sh.lianjia.com/ershoufang/sh4680593.html"
    i1 = link.rfind("/")
    ret = link[i1 + 1:len(link) - 5]
    print(ret)
    return ret

if(__name__ == "__main__"):
    # testGetId
    # testList()
    # testTime()
    pass
