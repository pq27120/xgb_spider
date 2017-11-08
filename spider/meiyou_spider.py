# -*- coding: utf-8 -*-
import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import rest_util

UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

class MeiYouSpider(object):
    def __init__(self):
        self.base_url = 'http://120.78.132.250:8084/admin_api'
        self.headers = {'content-type': 'application/json;charset=utf8', 'Connection': 'close'}
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            UA
        )
        dcap["takesScreenshot"] = (False)
        self.driver = webdriver.PhantomJS(executable_path=r"D:\soft\phantomjs-2.1.1-windows\bin\phantomjs.exe", desired_capabilities=dcap, service_args=['--load-images=no'])
        self.api_util = rest_util.RestUtil()

    def get_article_list(self, url):
        '''
        使用phantomjs下载文章
        :param url: 文章链接
        :return:
        '''
        if url is None:
            return None
        else:
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url)
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                page_list = soup.find_all('div', class_="news-item", limit=20)
                return page_list
            except:
                print(url)


    def get_article_detail(self, url):
        '''
        使用phantomjs下载文章
        :param url: 文章链接
        :return:
        '''
        if url is None:
            return None
        else:
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url)
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                page_detail = soup.find('div', class_="detail")
                return page_detail
            except:
                print(url)

    def process_meiyou_article(self, url, tab, parent_id, page_no):
        list = self.get_article_list(url + '?parent_id=' + parent_id + '&page_no=' + page_no)
        for article in list:
            soup = BeautifulSoup(str(article), 'html.parser', from_encoding='utf-8')
            title = soup.find('div', class_='news-outline').find('a').get_text().strip(' \n').encode('utf-8')
            is_repeat = self.his_repeat(title)
            if is_repeat is False:
                conver_image = soup.find('div', class_='news-thumb').find('img')['src']
                url = soup.find('div', class_='news-thumb').find('a')['href']
                content = self.get_article_detail('http://www.meiyou.com' + url)
                self.api_util.add_new_topic(title, str(content), conver_image, tab)

    def his_repeat(self, title):
        payload = {'title': title}
        url = self.base_url + '/spider/judgeIsSpider'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['is_spider']

    def __del__(self):
        self.driver.quit()

if __name__ == '__main__':
    meiyou = MeiYouSpider()
    print meiyou.process_meiyou_article('http://www.meiyou.com/zhishi/beiyun', '怀孕', '4', '1')
