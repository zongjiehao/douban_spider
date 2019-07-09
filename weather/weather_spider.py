# encoding:utf-8
# author:haozj 
# create_time: 2019/7/8

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36"
}


def parse_html(url):
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('utf-8')
    soup = BeautifulSoup(text, 'lxml')
    conMidtab = soup.find_all('div', class_='conMidtab')[1]
    print(conMidtab)



def main():
    url = 'http://www.weather.com.cn/textFC/hb.shtml'
    parse_html(url)


if __name__ == '__main__':
    main()
