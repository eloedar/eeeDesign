# 导入requests包
import requests


# url = "https://sctapi.ftqq.com/SCT165116TqneFO2PJ7lMcDgDsXQHXTixD.send?title=messagetitle"
# myParams = {"title": "TestMessage", "desp": "This is a test message"}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
# res = requests.get(url=url, params=myParams)

# print('url:', res.request.url)  # 查看发送的url
# print("response:", res.text)  # 返回请求结果32

def wechat_send(text):
    url = "https://sctapi.ftqq.com/SCT165116TqneFO2PJ7lMcDgDsXQHXTixD.send?title=messagetitle"
    myParams = {"title": text, "desp": "Hand gesture" + text + "detected! "}  # 字典格式，推荐使用，它会自动帮你按照k-v拼接url
    res = requests.get(url=url, params=myParams)
    print('url:', res.request.url)  # 查看发送的url
    print("response:", res.text)  # 返回请求结果32
