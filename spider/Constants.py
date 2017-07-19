import queue

LIANJIA_ID = "lianjiaId"

LIANJIA_HOST = "http://sh.lianjia.com"

#工作模式，1位正常
FLAG = 1

pending_urls = queue.Queue()

estateMap = dict()

proxys = []

failedProxys = []

