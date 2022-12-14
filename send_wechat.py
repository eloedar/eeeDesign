# 导入requests包
import requests
from duo import read_dht11_dat


# url = "https://sctapi.ftqq.com/SCT165116TqneFO2PJ7lMcDgDsXQHXTixD.send?title=messagetitle"
# myParams = {"title": "TestMessage", "desp": "This is a test message"}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
# res = requests.get(url=url, params=myParams)

# print('url:', res.request.url)  # 查看发送的url
# print("response:", res.text)  # 返回请求结果32

def wechat_send(text):
    urls = ["https://sctapi.ftqq.com/SCT165116TqneFO2PJ7lMcDgDsXQHXTixD.send?title=messagetitle",
            "https://sctapi.ftqq.com/SCT165257ThlcIj28JPnCD0WCQUdxS9kIb.send?title=messagetitle"]
    url_i = "http://open.iciba.com/dsapi/"
    r = requests.get(url_i)
    content = r.json()['content']
    note = r.json()['note']

    result = read_dht11_dat()
    if result:
        temperature, humidity = result
        myParams = {"title": "提醒事项",
                    "desp": text + "今天的气温是%s摄氏度, 今天的湿度是: %s %% . "
                                   "祝你度过美好一天！ 今日必应美图： "
                                   ""
                                   "![Bing](https://www.todaybing.com/api/today/cn)"
                                   "每日格言：%s " % (
                                humidity, temperature, content)}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
        for url in urls:
            res = requests.get(url=url, params=myParams)
    else:
        myParams = {"title": "提醒事项",
                    "desp": text + "今天的气温以及湿度无法获取，可能是传感器故障。 "
                                   "祝你度过美好一天！ 今日必应美图： "
                                   ""
                                   "![Bing](https://www.todaybing.com/api/today/cn)"
                                   "每日格言：%s" % content}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url

        for url in urls:
            res = requests.get(url=url, params=myParams)


wechat_send("你好！开盖手势已经被识别到。")
