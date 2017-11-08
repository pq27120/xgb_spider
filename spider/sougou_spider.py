# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import time
import requests
import wechatsogou
from jdbc_util import *
import html_downloader
from spider import html_parser


class SpiderSouGou(object):
    def __init__(self):
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.headers = {'content-type': 'application/json;charset=utf8', 'Connection': 'close'}
        self.base_url = 'http://120.78.132.250:8084/admin_api'
        # self.base_url = 'http://127.0.0.1:8084/admin_api'


    def spider_weichat(self, name):
        ws_api = wechatsogou.WechatSogouAPI(captcha_break_time=10)
        gzh_info = ws_api.search_article(name)
        return gzh_info

    def get_sprider_source(self):
        source_list = self.spider_source_list()
        for source in list(source_list):
            if source['channel'] == '1':
                time.sleep(2)
                gzh_list = self.spider_weichat(source['name'])
                for gzh_info in gzh_list:
                    title = gzh_info['article']['title'].decode("UTF-8")
                    url = gzh_info['article']['url']
                    is_repeat = self.his_repeat(title)
                    if is_repeat is False:
                        html = self.downloader.download_articles_ph(url)
                        data = self.parser.parse_article(html)
                        if data is None:
                            continue

                        imageUrl = self.process_head_image(gzh_info['article']['imgs'])
                        (article_title, wname, date, content) = data
                        is_repeat = self.his_repeat(article_title)
                        if is_repeat is False:
                            content = content.encode("UTF-8")

                            self.add_new_topic(article_title, content, imageUrl)
            if source['channel'] == '2':
                time.sleep(1)


    def process_head_image(self, image_obj):
        if len(image_obj):
            if type(image_obj[0]) == list:
                image_url = image_obj[0][0]
            else:
                image_url = image_obj[0]
            if image_url is not None:
                image_url = image_url[image_url.find('url=') + 4:]
                return image_url

    def his_repeat(self, title):
        payload = {'title': title}
        url = self.base_url + '/spider/judgeIsSpider'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['is_spider']

    def add_new_topic(self, title, content, cover_image):
        payload = {'title': title, 'content': content, 'coverImage': cover_image}
        url = self.base_url + '/spider/addTopic'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['save_result']

    def spider_source_list(self):

        url = self.base_url + '/spider/spiderSourceList'
        r = requests.post(url, data={}, headers=self.headers)
        return r.json()['source_list']

if __name__ == '__main__':
    sougou = SpiderSouGou()
    sougou.get_sprider_source()

