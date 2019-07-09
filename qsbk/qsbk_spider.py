# encoding:utf-8
# author:haozj
# create_time: 2019/6/30
import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"
}
url = "https://www.qiushibaike.com/text/"
response = requests.get(url, headers=headers)
text = response.text
html = etree.HTML(text)
div = html.xpath("//div[@class='article block untagged mb15 typs_hot']/a/@href")
new_div = list(set(div))

new_div.sort(key=div.index)
for i in new_div:
    homepage = "https://www.qiushibaike.com" + str(i)
    print(homepage)
    response1 = requests.get(homepage, headers=headers)
    text = response1.text
    html1 = etree.HTML(text)
    # title = html1.xpath("//h1[@class='article-title']/text()")[0]
    # print(title)
    content = html1.xpath("//div[@class='content']//text()")
    print(str(content).replace('[', '').replace(']', ''))
