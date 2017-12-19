# -*- coding: UTF-8 -*-
import json

import requests


class RestUtil(object):
    def __init__(self):
        self.headers = {'content-type': 'application/json;charset=utf8', 'Connection': 'close'}
        # self.base_url = 'http://127.0.0.1:8084/admin_api'
        self.base_url = 'http://120.78.132.250:8084/admin_api'

    def add_new_topic(self, title, content, cover_image, tab, channel, sub_title):
        payload = {'title': title, 'content': content, 'coverImage': cover_image, 'tab': tab, 'channel': channel, 'subTitle': sub_title}
        url = self.base_url + '/spider/addTopic'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['save_result']

    def update_topic(self, topic_id, cover_image, content):
        payload = {'id': topic_id, 'content': content, 'coverImage': cover_image}
        url = self.base_url + '/spider/updateTopic'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['save_result']

    def spider_source_list(self):
        url = self.base_url + '/spider/spiderSourceList'
        r = requests.post(url, data={}, headers=self.headers)
        return r.json()['source_list']

    def spider_his_list(self, image_process):
        payload = {'imageProcess': image_process}
        url = self.base_url + '/spider/spiderHisList'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['his_list']

    def spider_topic(self, topic_id):
        url = self.base_url + '/spider/topicInfo'
        r = requests.get(url + '?id=' + str(topic_id), headers=self.headers)
        return r.json()['topic']