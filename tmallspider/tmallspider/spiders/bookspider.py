from __future__ import absolute_import
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import scrapy
from selenium.webdriver import ActionChains
from tmallspider.items import TmallspiderItem
from tmallspider.items import JdspiderItem
from tmallspider.items import SnspiderItem
from tmallspider.items import DdspiderItem
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerRunner, CrawlerProcess
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

def encodeGB2312(data):
    hexData = data.encode(encoding='GB2312').hex().upper()
    encoded = '%' + '%'.join(hexData[i:i + 2] for i in range(0, len(hexData), 2))
    return encoded

s_input = 'oppo reno 4 pro'

class tmallSpider(scrapy.Spider):
    name = 'tttspider'
    start_urls = [
        'http://login.tmall.com'
    ]

    items = TmallspiderItem()

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.switch_to.frame(self.driver.find_element_by_id('J_loginIframe'))
        self.driver.find_element_by_name('fm-login-id').send_keys('iamgooglepenn')
        self.driver.find_element_by_id('fm-login-password').send_keys('Hello_World2019')
        time.sleep(2)
        source_element = self.driver.find_element_by_id('nc_1_n1z')
        ActionChains(self.driver).drag_and_drop_by_offset(source_element, 270, 0).perform()
        time.sleep(1)
        self.driver.find_element_by_class_name('fm-btn').click()
        #fm-button fm-submit password-login
        time.sleep(5)
        self.driver.find_element_by_name('q').send_keys(s_input)
        time.sleep(2)
        self.driver.find_element_by_css_selector('button').click()
        n = 0

        for element in WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.product-iWrap'))):
            if n < 5:
                n += 1
                #if yanzheng == 0:
                #    yanzheng += 1
                #    self.driver.switch_to.frame(self.driver.find_element_by_id('sufei-dialog-content'))
                #    source_element = self.driver.find_element_by_id('nc_1_n1z')
                #    ActionChains(self.driver).drag_and_drop_by_offset(source_element, 260, 0).perform()
                time.sleep(2)
                product_name_tmall = element.find_element_by_css_selector('.productTitle a')
                product_price_tmall = element.find_element_by_css_selector('.productPrice em')
                tmallSpider.items['product_name_tmall'] = product_name_tmall.get_attribute('title')
                tmallSpider.items['product_price_tmall'] = product_price_tmall.get_attribute('title')

                home_page = self.driver.window_handles[0]
                element.click()
                window_detail = self.driver.window_handles[n]
                self.driver.switch_to_window(window_detail)
                try:
                    time.sleep(2)
                    product_disount_tmall = self.driver.find_element_by_css_selector('.tm-gold dd').text
                    tmallSpider.items['product_discount_tmall'] = product_disount_tmall
                except NoSuchElementException:
                    tmallSpider.items['product_discount_tmall'] = 'no discount'
                yield tmallSpider.items
                self.driver.switch_to_window(home_page)

class jdSpider(scrapy.Spider):
    name = 'jjjspider'
    start_urls = [
        'http://jd.com'
    ]
    items = JdspiderItem()

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('key').send_keys(s_input)
        time.sleep(2)
        self.driver.find_element_by_css_selector('.button').click()
        n = 0
        for element in WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.gl-i-wrap'))):
            click_item = self.driver.find_element_by_class_name('p-img')
            if n < 6:
                n += 1
                time.sleep(2)

                product_name_jd = element.find_element_by_css_selector('.p-name-type-2').text
                product_name_jd = product_name_jd.split('"')[-1].strip()
                product_price_jd = element.find_element_by_css_selector('.p-price i').text
                jdSpider.items['product_name_jd'] = product_name_jd
                jdSpider.items['product_price_jd'] = product_price_jd

                home_page = self.driver.window_handles[0]
                click_item.click()
                print('aaaaaa')
                print(n)
                time.sleep(2)
                window_detail = self.driver.window_handles[n]
                self.driver.switch_to_window(window_detail)
                try:
                    product_discount_jd = self.driver.find_element_by_css_selector('#summary-quan .text').text
                    jdSpider.items['product_discount_jd'] = product_discount_jd
                except NoSuchElementException:
                    jdSpider.items['product_discount_jd'] = 'no discount'
                yield jdSpider.items
                self.driver.switch_to_window(home_page)

class ddSpider(scrapy.Spider):
    name = 'dddspider'
    start_urls = [
        'http://www.dangdang.com'
    ]
    items = DdspiderItem()

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('key_S').send_keys(s_input)
        time.sleep(1)
        self.driver.find_element_by_css_selector('.button').click()
        n = 0
        for element in WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#component_59 li'))):
            if n < 5:
                n += 1
                product_name_dd = element.find_element_by_css_selector('.name a , .skcolor_ljg').text
                product_price_dd = element.find_element_by_css_selector('.search_now_price').text
                try:
                    product_discount_dd = element.find_element_by_css_selector('.new_lable2').text
                except NoSuchElementException:
                    product_discount_dd = 'no discount'
                ddSpider.items['product_name_dd'] = product_name_dd
                ddSpider.items['product_price_dd'] = product_price_dd
                ddSpider.items['product_discount_dd'] = product_discount_dd
                yield ddSpider.items

class snSpider(scrapy.Spider):
    name = 'ssnspider'

    start_urls = [
       'https://www.suning.com/'
    ]
    items = SnspiderItem()
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('searchKeywords').send_keys(s_input)
        time.sleep(1)
        self.driver.find_element_by_id('searchSubmit').click()
        n = 0
        home_page = self.driver.window_handles[0]
        for element in WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.item-bg'))):
            if n < 5:
                n += 1
                time.sleep(2)
                element.click()
                window_detail = self.driver.window_handles[n]
                self.driver.switch_to_window(window_detail)
                product_name_sn = self.driver.find_element_by_css_selector('#itemDisplayName').text
                product_price_sn = self.driver.find_element_by_css_selector('.mainprice').text
                snSpider.items['product_name_sn'] = product_name_sn
                snSpider.items['product_price_sn'] = product_price_sn
                try:
                    product_discount_sn_list = self.driver.find_elements_by_css_selector('.p-quan-white')
                    product_discount_sn = ''
                    for i in range(len(product_discount_sn_list)):
                        product_discount_sn += product_discount_sn_list[i].text
                    snSpider.items['product_discount_sn'] = product_discount_sn
                except NoSuchElementException:
                    snSpider.items['product_discount_sn'] = 'no discount'
                yield snSpider.items
                self.driver.switch_to_window(home_page)

'''
process = CrawlerProcess(settings={
    "FEEDS": {
        "tmallitem.csv": {"format": "csv", 'fields': ['product_name_tmall', 'product_price_tmall', 'product_discount_tmall'],},
        "jditem.csv": {"format": "csv", 'fields': ['product_name_jd', 'product_price_jd', 'product_discount_jd'],},
        "snitem.csv": {"format": "csv", 'fields': ['product_name_sn', 'product_price_sn', 'product_discount_sn'],},
        "dditem.csv": {"format": "csv", 'fields': ['product_name_dd', 'product_price_dd', 'product_discount_dd'],},
    },
})

process.crawl(tmallSpider)
process.crawl(jdSpider)
process.crawl(snSpider)
process.crawl(ddSpider)
process.start()
'''