# encoding:utf-8
# author:haozj 
# create_time: 2019/7/3
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/75.0.3770.100 Safari/537.36",
    "referer": "https://careers.tencent.com/",
    "cookie": "_ga=GA1.2.1835781157.1547904510; pgv_pvi=4833776640; _gcl_au=1.1.2111773658.1557587013",
    "upgrade-insecure-requests": "1"

}

url = "https://careers.tencent.com/search.html?index=2&keyword=python"


def get_detail_url(url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    soup = BeautifulSoup(text, 'lxml')
    print(soup.find_all('a', class_='recruit-list-link'))


get_detail_url(url)

# def spider():
#     url = 'https://careers.tencent.com/search.html?index={}&keyword=python'
#     for i in range(1, 2):
#         url = url.format(i)
#         get_detail_url(url)
#
#
# spider()
