# encoding:utf-8
# author:haozj 
# create_time: 2019/6/30
from lxml import etree
import requests
import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"
}
url = "https://www.ygdy8.net/html/gndy/dyzz/index.html"
BASE_URL = "https://www.ygdy8.net"


# 获取详情页
def get_detail_urls(url):
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'gbk'
    text = response.text
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a[@class='ulink']/@href")
    detail_urls = map(lambda url: BASE_URL + url, detail_urls)
    return detail_urls


# 解析详情页
def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=HEADERS)
    response.encoding = 'gbk'
    text = response.text
    html = etree.HTML(text)
    title = html.xpath("//font[@color='#07519a']/text()")[0]
    imgs = html.xpath("//div[@id='Zoom']//img/@src")
    cover = imgs[0]
    screenshot = imgs[1]
    movie['title'] = title
    movie['cover'] = cover
    movie['screenshot'] = screenshot
    infos = html.xpath("//div[@id='Zoom']//text()")
    for index, info in enumerate(infos):
        if info.startswith("◎年　　代"):
            movie['year'] = parse_info(info, "◎年　　代")
        elif info.startswith("◎产　　地"):
            movie['country'] = parse_info(info, "◎产　　地")
        elif info.startswith("◎类　　别"):
            movie['type'] = parse_info(info, "◎类　　别")
        elif info.startswith("◎豆瓣评分"):
            movie['score'] = parse_info(info, "◎豆瓣评分")
        elif info.startswith("◎主　　演"):
            actors = []
            info = parse_info(info, "◎主　　演")
            actors.append(info)
            for x in range(index + 1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎简　　介"):
                    break
                actors.append(actor)
            movie['actors'] = actors
        elif info.startswith("◎简　　介"):
            # profiles = []
            for x in range(index + 1, index+2):
                profile = infos[x].strip()
                # profiles.append(profile)
            movie['profile'] = profile
    download_url = html.xpath("//td[@bgcolor='#fdfddf']//text()")[0]
    movie['download_url'] = download_url
    return movie


def parse_info(info, rule):
    return info.replace(rule, "").strip()


# 爬取信息
def spider():
    url = "https://www.ygdy8.net/html/gndy/dyzz/list_23_{}.html"
    movies = []
    for x in range(1, 2):
        url = url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            print(detail_url)
            movie = parse_detail_page(detail_url)
            movies.append(movie)
    with open('movie.txt', 'a', encoding='utf-8') as fp:
        fp.write(json.dumps(movies, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    spider()
