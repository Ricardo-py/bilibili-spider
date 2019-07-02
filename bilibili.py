import requests
import json
import base64
import pymongo
import time
from multiprocessing import Pool

global total
total = 1

#查最大值：db.person.find({}).sort({"num" : -1}).limit(1)


def get_proxies_2():
    url = "https://proxy.horocn.com/api/proxies?order_id=5XPC1637821784969771&num=1&format=json&line_separator=win&can_repeat=no"
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

def spider(ran,mycol):
    print("kaishi")
    flag = True
    proxies = {
        "http": "http://115.226.145.205:28437",
        "https": "https://115.226.145.205:28437",
    }
    for i in range(ran[0],ran[1]):
        while(True):
            url = 'https://api.bilibili.com/x/web-interface/card?mid=' + str(i) + '&photo=true'
            #url='https://www.baidu.com'
            try:
                while (True):
                    if (flag == False):
                        proxies = get_proxies_2()
                        print('更换代理')
                        print(proxies)
                    data = requests.get(url=url,proxies=proxies,timeout=10)
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
    return


if __name__ == '__main__':
    print(int("154784646"))
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient['bilibili-fans']
    mycol = mydb['sites']
    record = mycol.find().sort("num",-1).limit(1)
    if (record.count() != 0):
        for temp in record:
            print("数据库中的最大值为:"+str(temp['num']))
            start = temp['num'] + 1
    else:
        start = 1
    spider([start,5000000000],mycol)
    # proxies = {
    #     "http":"http://59.33.136.130:28526",
    #     "https":"https://59.33.136.130:28526",
    # }
    # result = requests.get(url="http://httpbin.org/get",proxies=proxies,timeout=3)
    # print(result.text)


