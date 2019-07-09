# encoding:utf-8
# author:haozj 
# create_time: 2019/6/29
import requests
from lxml import etree

# 1.抓取页面
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36",
    "Referer": "https://movie.douban.com/"
}
url = 'https://movie.douban.com/cinema/nowplaying/beijing/'
# 2，提取数据
response = requests.get(url=url, headers=headers)
text = response.text
# print(response.content.decode('utf-8'))
html = etree.HTML(text)
ul = html.xpath("//ul[@class='lists']")[0]
lists = ul.xpath("./li")
movies = []
for li in lists:
    title = li.xpath("@data-title")[0]
    score = li.xpath("@data-score")[0]
    duration = li.xpath("@data-duration")[0]
    region = li.xpath("@data-region")[0]
    director = li.xpath("@data-director")[0]
    actors = li.xpath("@data-actors")[0]
    poster = li.xpath(".//img/@src")[0]
    with open('movie_txt.txt', 'a', encoding='utf-8') as fp:
        fp.write('\n'.join([title, score, duration, region, director, actors, poster]))
        fp.write('\n'+"*"*50+"\n")
