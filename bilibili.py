import requests
import json
import base64
import time
from multiprocessing import Pool

global total
total = 1



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

def spider(ran):
    print("kaishi")
    flag = False
    proxies = ""
    for i in range(ran[0],ran[1]):
        while(True):
            url = 'https://api.bilibili.com/x/web-interface/card?mid=' + str(i) + '&photo=true'
            #url='https://www.baidu.com'
            try:
                while (True):
                    if (flag == False):
                        proxies = {
                            "http":"http://183.166.6.242:26577",
                            "https":"https://183.166.6.242:26577",
                    }
                    print(proxies)
                    data = requests.get(url=url,proxies=proxies,timeout=5)
                    print("有问题")
                    if (data.status_code == 200):
                        flag = True
                        print("有效的代理")
                        break
                    else:
                        flag = False
                        print(data.status_code)
                        tt = requests.get(url="http://httpbin.org/get", proxies=proxies)
                        print(tt.text)
                break
            except:
                print('继续')
        if (data.status_code == 200):
            result = data.text
            js = json.loads(result)
            if (js['code'] == 0):
                fannum = js['data']['card']['fans']
                Name = js['data']['card']['name']
                number = js['data']['card']['mid'];
                print("编号: " + str(number) + "昵称：" + str(Name) + "粉丝数量：" + str(fannum))
    return


if __name__ == '__main__':
    #spider([1,2000])
    # start_time = time.time()
    # pool = Pool(processes=4)
    # canshu1 = [1,500]
    # canshu2 = [501,1000]
    # canshu3 = [1001,1500]
    # canshu4 = [1501,2000]
    # pool.map(spider,zip(canshu1,canshu2,canshu3,canshu4))
    # end_time = time.time()
    # print("耗时:",end_time-start_time)
    #proxy = requests.get("https://proxy.horocn.com/api/proxies?order_id=5XPC1637821784969771&num=10&format=json&line_separator=win&can_repeat=no")
    #js = json.loads(proxy.text)

    # for temp in js:
    #     prox = "https://" + temp['host'] + ":" + temp['port']
    #     prox2 = "http://" + temp['host'] + ":" + temp['port']
    #     proxies = {}
    #     proxies["https:"] = prox
    #     proxies["http:"] = prox2
    #     print(proxies)
    # proxies = get_proxies()
    proxies = {
        "http":"http://180.122.144.195:45689",
        "https":"https://180.122.144.195:45689",
    }
    result = requests.get(url="http://httpbin.org/get",proxies=proxies,timeout=1)
    print(result.text)


