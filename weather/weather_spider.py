# encoding:utf-8
# author:haozj 
# create_time: 2019/7/8

import requests
from bs4 import BeautifulSoup
from pyecharts import Bar
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"
}

ALL_DATA = []


def parse_html(url):
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, 'html5lib')
    conMidtab = soup.find_all('div', class_='conMidtab')[1]
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')[0]
            if index == 0:
                tds = tr.find_all('td')[1]
            city = list(tds.stripped_strings)[0]
            tems = tr.find_all('td')[-5]
            temp = list(tems.stripped_strings)[0]
            ALL_DATA.append({"city": city, "temp": int(temp)})


def main():
    urls = ['hb', 'db', 'hd', 'hz', 'hn', 'xb', 'xn', 'gat']
    for i in urls:
        url = 'http://www.weather.com.cn/textFC/{0}.shtml'.format(i)
        parse_html(url)

    ALL_DATA.sort(key=lambda x: x['temp'], reverse=True)
    data = ALL_DATA[0:10]
    print(type(data))
    # print(data)
    citys = list(map(lambda x: x['city'], data))
    temps = list(map(lambda x: x['temp'], data))
    bar = Bar("全国高温排行榜")
    bar.add('', citys, temps)
    bar.render('temp.html')


if __name__ == '__main__':
    main()
