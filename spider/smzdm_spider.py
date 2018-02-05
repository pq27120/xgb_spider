# -*- coding: utf-8 -*-
import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import rest_util

UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"

class SMZDM_Spider(object):
    def __init__(self):
        self.base_url = 'http://120.78.132.250:8084/admin_api'
        self.headers = {'content-type': 'application/json;charset=utf8', 'Connection': 'close'}
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            UA
        )
        dcap["takesScreenshot"] = (False)
        # self.driver = webdriver.PhantomJS(executable_path=r"D:\soft\phantomjs-2.1.1-windows\bin\phantomjs.exe", desired_capabilities=dcap, service_args=['--load-images=no'])
        self.driver = webdriver.PhantomJS(executable_path=r"/usr/local/phantomjs/bin/phantomjs", desired_capabilities=dcap,
                                          service_args=['--load-images=no'])
        self.api_util = rest_util.RestUtil()

    def process_smzdm_article(self, url):
        try:
            page_list, page_list1 = self.get_article_list(url)
            self.process_smzdm_article_detail(page_list)
            self.process_smzdm_article_detail(page_list1)
            self.driver.quit()
        except:
            self.driver.quit()

    def process_smzdm_article_detail(self, list):
        for article in list:
            soup = BeautifulSoup(str(article), 'html.parser', from_encoding='utf-8')
            title = soup.find('div', class_='z-feed-title').find('a').get_text().strip(' \n').encode('utf-8')
            sub_title = soup.find('div', class_='z-feed-foot-l').find('span').get_text().strip(' \n').encode('utf-8')
            is_repeat = self.his_repeat(title)
            if is_repeat is False:
                conver_image = soup.find('div', class_='z-feed-img').find('img')['src']
                url = soup.find('div', class_='z-feed-img').find('a')['href']
                # content = self.get_article_detail(url)
                content = url.replace('www', 'm')
                self.api_util.add_new_topic(title, str(content), conver_image, '优惠', '3', sub_title)

    def get_article_list(self, url):
        if url is None:
            return None
        else:
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url)
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                page_list = soup.find_all('li', class_="z-hor-feed feed-hor rank-item-hot")
                page_list1 = soup.find_all('li', class_="z-hor-feed feed-hor rank-item")
                return page_list, page_list1
            except:
                self.driver.quit()
                print(url)

    def get_article_detail(self, url):
        if url is None:
            return None
        else:
            try:
                self.driver.set_page_load_timeout(30)
                self.driver.get(url)
                time.sleep(1)
                html = self.driver.page_source
                soup = BeautifulSoup(html, 'html.parser', from_encoding='utf-8')
                page_detail = soup.find('div', class_="item-box item-preferential")
                return page_detail
            except:
                self.driver.quit()
                print(url)

    def his_repeat(self, title):
        payload = {'title': title}
        url = self.base_url + '/spider/judgeIsSpider'
        r = requests.post(url, data=json.dumps(payload), headers=self.headers)
        return r.json()['is_spider']

if __name__ == '__main__':
    smzdm = SMZDM_Spider()
    smzdm.process_smzdm_article('http://search.smzdm.com/?c=home&s=%E6%AF%8D%E5%A9%B4%E7%94%A8%E5%93%81&order=score')