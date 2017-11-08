# -*- coding: UTF-8 -*-
import os
import time

import requests

import rest_util
from bs4 import BeautifulSoup

class ImageProcess(object):
    def __init__(self):
        self.api_util = rest_util.RestUtil()
        self.base_dir = '/usr/share/nginx/html/images/wechat/'
        # self.base_dir = 'E:\\test\\'
        self.static_url = 'https://h5.xiaoguaibao.com/images/wechat/'

    def process_image(self):
        his_list = self.api_util.spider_his_list(1)
        for his in his_list:
            topic = self.api_util.spider_topic(str(his['id']))
            conver_image = topic['coverImage']
            if conver_image.startswith('http') is not True:
                conver_image = 'http:' + conver_image
                image = requests.get(conver_image)
                path = self.base_dir + str(topic['id'])
                isExists = os.path.exists(path)
                if isExists is not True:
                    os.makedirs(path)
                file_name = str(int(round(time.time()*1000))) + '_conver.jpg'
                with open(path + '/' + file_name, 'wb') as f:
                    f.write(image.content)

                    conver_image = self.static_url + str(topic['id']) + '/' + file_name
                    content = topic['content']
                    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
                    images = soup.find_all('img')
                    for image in images:
                        image_url = image['src']
                        if image_url.startswith('http') is not True:
                            image_url = 'http:' + image_url
                            content_image = requests.get(image_url)
                            content_file_name = str(int(round(time.time() * 1000))) + '.jpg'
                            with open(path + '/' + content_file_name, 'wb') as f:
                                f.write(content_image.content)
                                new_image_url = self.static_url + str(topic['id']) + '/' + content_file_name
                                content = content.replace(image['src'], new_image_url)

                    self.api_util.update_topic(topic['id'], conver_image, content)


if __name__ == '__main__':
    process = ImageProcess()
    process.process_image()