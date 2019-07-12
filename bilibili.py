import requests
import json
import base64
import pymongo
from queue import Queue
import threading
import time
import datetime
from multiprocessing import Pool

global total
total = 1
q = Queue()
before_time_proxies=0
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient['bilibili-fans']
mycol = mydb['sites']
#查最大值：db.person.find({}).sort({"num" : -1}).limit(1)

class MyThread(threading.Thread):
    def __init__(self,func,name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.name = name

    def run(self):
        self.func()


def get_proxies_2():
    url = "https://proxy.horocn.com/api/proxies?order_id=TRJ61638848116791140&num=1&format=json&line_separator=win&can_repeat=no"
    jsontext = json.loads(requests.get(url).text)
    for temp in jsontext:
        host = temp['host']
        port = temp['port']
    proxies = {}
    proxies["http"] = "http://" + host + ":" + port
    proxies["https"] = "https://" + host + ":" + port
    return proxies

def get_proxies():
    strr = "G3KV1637823384560299:qIcYzrkKaiESbkpV"
    encode_strr = base64.b64encode(strr.encode('utf-8'))
    header = {
        "Proxy - Authorization": "Basic"+"\n"+ str(encode_strr,'utf-8')
    }
    target_url = "http://httpbin.org/get"
    proxy_host = 'dyn.horocn.com'
    proxy_port = 50000
    proxy_username = 'G3KV1637823384560299'
    proxy_pwd = "qIcYzrkKaiESbkpV"

    proxies = {
        'http': 'http://{}:{}@{}:{}'.format(proxy_username, proxy_pwd, proxy_host, proxy_port),
    }
    return proxies

def spider_all():
    print("kaishi")
    flag = True
    proxies = {
        "http": "http://115.226.145.205:28437",
        "https": "https://115.226.145.205:28437",
    }
    while True:
        if (~q.empty()):
            i = q.get(1)
            while (True):
                url = 'https://api.bilibili.com/x/web-interface/card?mid=' + str(i) + '&photo=true'
                # url='https://www.baidu.com'
                try:
                    while (True):
                        if (flag == False):
                            global before_time_proxies
                            now_time = datetime.datetime.now()
                            if (now_time - before_time_proxies).seconds < 10:
                                time.sleep(10)
                            before_time_proxies = now_time
                            print('更换代理')
                            proxies = get_proxies_2()
                            # print('更换代理')
                            print(proxies)
                        data = requests.get(url=url, proxies=proxies, timeout=10)
                        if (data.status_code == 200):
                            flag = True
                            break
                        else:
                            flag = False
                    break
                except Exception as e:
                    flag = False
                    print(e)
                    print('继续')
            if (data.status_code == 200):
                result = data.text
                js = json.loads(result)
                if (js['code'] == 0):
                    mydict = {}
                    fannum = js['data']['card']['fans']
                    Name = js['data']['card']['name']
                    number = js['data']['card']['mid']
                    mydict['fannum'] = fannum
                    mydict['name'] = Name
                    mydict['num'] = int(number)
                    print("编号: " + str(number) + "昵称：" + str(Name) + "粉丝数量：" + str(fannum))
                    mycol.insert_one(mydict)
        else:
            break
    return

# def spider_all():
#     while True:
#         if (~q.empty()):
#             i = q.get(1)
#             spider_onepage(int(i))
#         else:
#             break


if __name__ == '__main__':
    before_time_proxies = datetime.datetime.now()
    record = mycol.find().sort("num",-1).limit(1)
    if (record.count() != 0):
        for temp in record:
            print("数据库中的最大值为:"+str(temp['num']))
            start = temp['num'] + 1
    else:
        start = 1
    loops = [1,2,3,4,5,6,7,8,9,10]
    for i in range(start,1000000):
        q.put(i)
    print("开始执行")
    threads = []
    nloops = range(len(loops))
    for i in nloops:
        t = MyThread(spider_all,spider_all.__name__)
        threads.append(t)

    for i in nloops:
        time.sleep(10)
        threads[i].start()

    for i in nloops:
        threads[i].join()
    # proxies = {
    #     "http":"http://59.33.136.130:28526",
    #     "https":"https://59.33.136.130:28526",
    # }
    # result = requests.get(url="http://httpbin.org/get",proxies=proxies,timeout=3)
    # print(result.text)


