# encoding:utf-8
# author:haozj 
# create_time: 2019/8/3
import threading
import requests
from lxml import etree
from urllib import request
import os
import re
from queue import Queue
import time


class Producer(threading.Thread):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36"
    }

    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Producer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty():
                print('生产者空的')
                break
            url = self.page_queue.get()
            self.parse_url(url)

    def parse_url(self, url):
        response = requests.get(url, headers=self.headers)
        text = response.text
        html = etree.HTML(text)
        imgs = html.xpath("//div[@class='page-content text-center']//img[@referrerpolicy='no-referrer']")
        for img in imgs:
            img_url = img.get("data-original")
            alt = img.get("alt")
            alt = re.sub(r'[\?？.,，。！:]', '', alt)
            suffix = os.path.splitext(img_url)[1]
            filename = alt + suffix
            # if not os.path.exists('images'):
            #     os.mkdir('images')
            # request.urlretrieve(img_url, 'images/' + filename)
            self.img_queue.put((img_url, filename))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue, *args, **kwargs):
        super(Consumer, self).__init__(*args, **kwargs)
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        while True:
            if self.page_queue.empty() and self.img_queue.empty():
                print('消费者空的')
                return
            img= self.img_queue.get()
            url,filename = img
            request.urlretrieve(url, 'images/' + filename)
            print(filename+"下载完成！")


def main():
    page_queue = Queue(30)
    img_queue = Queue(1000)
    for i in range(1, 31):
        url = "http://www.doutula.com/photo/list/?page=%s" % i
        page_queue.put(url)

    for x in range(5):
        p = Producer(page_queue, img_queue)
        p.start()

    for x in range(5):
        c = Consumer(page_queue, img_queue)
        c.start()


if __name__ == '__main__':
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    main()
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    # parse_url("http://www.doutula.com/photo/list/?page=1")
