# encoding:utf-8
# author:haozj 
# create_time: 2019/8/3
import threading
import requests
from lxml import etree
from urllib import request
import os
import re
import time


def parse_url(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    text = response.text
    html = etree.HTML(text)
    imgs = html.xpath("//div[@class='page-content text-center']//img[@referrerpolicy='no-referrer']")
    for img in imgs:
        img_url = img.get("data-original")
        alt = img.get("alt")
        alt = re.sub(r'[\?？.,，。！:]', '', alt)
        suffix = os.path.splitext(img_url)[1]
        filename = alt + suffix
        if not os.path.exists('images'):
            os.mkdir('images')
        request.urlretrieve(img_url, 'images/' + filename)


def main():
    for i in range(1, 30):
        url = "http://www.doutula.com/photo/list/?page=%s" % i
        parse_url(url)


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    main()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # parse_url("http://www.doutula.com/photo/list/?page=1")

#2019-08-04 00:13:45
#2019-08-04 00:16:21