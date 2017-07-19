
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

if(__name__ == "__main__"):
    # testGetId
    testList()
    pass
