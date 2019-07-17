# encoding:utf-8
# author:haozj 
# create_time: 2019/7/15

import requests
import re


def get_one_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.100 Safari/537.36",
        'Connection': 'close'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return None

def parse_one_page(html):
    pattern = re.compile(
        '<i.*?class="board-index.*?">(.*?)</i>.*?<img.*?data-src="(.*?)".*?>.*?<p.*?class="name".*?<a.*?>(.*?)</a>.*?'
        '<p.*?class="star">(.*?)</p>.*?<p.*?class="releasetime">(.*?)</p>.*?<p\sclass="score"><.*?>(.*?)</i>.*?'
        '<i.*?class="fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'rank': item[0],
            'img': item[1],
            'name': item[2].strip(),
            'actor': item[3].strip()[3:] if len(item[3]) > 3 else '',
            'time': item[4].strip()[5:] if len(item[4]) > 5 else '',
            'score': item[5].strip() + item[6].strip()
        }

def main():
    for i in range(1):
        html = get_one_page("https://maoyan.com/board/4?offset={}".format(i * 10))
        for item in parse_one_page(html):
            print(item)
        # # 排名
        # rank = re.findall(r'<i\sclass="board-index.*?">(.*?)</i>', html, re.S)
        # # 图片
        # img = re.findall(r'<img.*?data-src="(.*?)".*?>', html, re.S)
        # # 名称
        # name = re.findall(r'<p\sclass="name".*?<a.*?>(.*?)</a>', html, re.S)
        # # 主演
        # actors = re.findall(r'<p\sclass="star">(.*?)</p>', html, re.S)
        # # 发布时间
        # release_time = re.findall(r'<p\sclass="releasetime">(.*?)</p>', html, re.S)
        # # 评分
        # integer = re.findall(r'<p\sclass="score"><.*?>(.*?)</i>', html, re.S)
        # fraction = re.findall(r'<p\sclass="score">.*?<i\sclass="fraction">(.*?)</i>', html, re.S)
        # print(fraction)



if __name__ == '__main__':
    main()
