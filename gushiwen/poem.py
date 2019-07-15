# encoding:utf-8
# author:haozj 
# create_time: 2019/7/14
import re
import requests
import json
# encoding:utf-8
# author:haozj
# create_time: 2019/7/8

import requests
import time
from bs4 import BeautifulSoup
from pyecharts import Bar

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36",
    'Connection': 'close'
}


def parse_html(url):
    response = requests.get(url, headers=HEADERS)
    html = response.text
    titles = re.findall(r'<div\sclass="cont">.*?<b>(.*?)</b>', html, re.DOTALL)
    dynasties = re.findall(r'<p\sclass="source">.*?<a.*?>(.*?)</a>', html, re.DOTALL)
    authors = re.findall(r'<p\sclass="source">.*?<a.*?>.*?<a.*?>(.*?)</a>', html, re.DOTALL)
    contents = re.findall(r'<div\sclass="contson".*?>(.*?)</div>', html, re.DOTALL)
    poems = []
    for content in contents:
        x = re.sub(r'<.*?>', "", content)
        poems.append(x.strip())

    gushis = []
    for value in zip(titles, dynasties, authors, poems):
        title, dynasty, author, poem = value
        gushi = {
            "title": title,
            "dynasty": dynasty,
            "author": author,
            "poem": poem
        }
        gushis.append(gushi)

    with open("gushi.txt", "a", encoding='utf-8') as fp:
        fp.write(json.dumps(gushis, indent=2, ensure_ascii=False))


def main():
    urls = "https://www.gushiwen.org/default_1.aspx"
    parse_html(urls)


if __name__ == '__main__':
    main()
