import requests
import pprint
import urllib
from urllib import parse
from pyquery import PyQuery as pq
from bs4 import BeautifulSoup


url1 = 'https://m.weibo.cn/api/container/getIndex?uid=3812602013&t=0&luicode=10000011&lfid=100103type=1&q=-1-tree&type=uid&value=3812602013&containerid=1076033812602013'
url2 = 'https://m.weibo.cn/api/container/getIndex?uid=3812602013&t=0&luicode=10000011&lfid=100103type=1&q=-1-tree&type=uid&value=3812602013&containerid=1076033812602013&since_id=4678506623271955'


# 主函数
def main():
    html = get_html()
    res = parase_html(html)
    print(res)  # 生成器对象
    print(next(res))
    print(next(res))


# 请求页面
def get_html():
    url = 'https://m.weibo.cn/api/container/getIndex?jumpfrom=weibocom&type=uid&value=3316261970&containerid=1076033316261970&since_id=4717673768030797'
    response = requests.get(url=url1)
    res = response.content  # 二进制文件,打印出来有'b',表示的是二进制bytes
    #print(type(res))
    res = response.text  # 字符串
    #print(type(res))
    res = response.json()
    #print(res)

    # ********************我是一条分界线*************************

    # post获取页面
    data = bytes(parse.urlencode({"hello": "world"}), encoding="utf-8")
    headers: {}
    # 防止别人知道我是爬虫
    request = urllib.request.Request(url=url, data=data, headers=headers, method="POST")
    try:
        response = urllib.request.urlopen(request)
        print(response.read().decode("utf-8"))
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    # 状态码
    print(response.status)
    print(response.getheaders())
    return res


# 解析数据
def parase_html(html):
    cards = html["data"]["cards"]
    for card in cards:
        xinna = {}
        mblog = card["mblog"]
        # pq().text()只保留文本,去除html标签
        xinna["内容"] = pq(mblog["text"]).text()
        xinna["评论"] = mblog["comments_count"]
        # 字符串格式化的方法
        # print(f"content:{con},comment:{comment}")
        print(xinna)
        yield xinna

# 超时处理
try:
    response = urllib.request.urlopen("http://httpbin.org/post", timeout=0.01)
    print(response.read().decode("utf-8"))
except urllib.error.URLError as e:
    print("timeout!")

if __name__ == "__main__":
    main()
