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

class tmallSpider(scrapy.Spider):
    name = 'ttspider'
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
        self.driver.find_element_by_name('q').send_keys('beats powerbeats pro')
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
    name = 'jjspider'
    start_urls = [
        'http://jd.com'
    ]
    items = JdspiderItem()

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('key').send_keys('beats powerbeats pro')
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
    name = 'ddspider'
    output = encodeGB2312('ipad air 3')
    start_urls = [
        'http://search.dangdang.com/?key={}&act=input'.format(output)
    ]

    def parse(self, response):
        open_in_browser(response)
        items = DdspiderItem()
        product_info = response.css('#component_59 li')
        for product in product_info:
            product_name_dd = product.css('.name a::attr(title)').extract()
            product_price_dd = product.css('.price_n::text').extract()
            items['product_name_dd'] = product_name_dd
            items['product_price_dd'] = product_price_dd
            yield items

class snSpider(scrapy.Spider):
    name = 'snspider'

    start_urls = [
       'https://www.suning.com/'
    ]
    items = SnspiderItem()
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.find_element_by_id('searchKeywords').send_keys('beats powerbeats pro')
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
                    product_discount_sn = self.driver.find_elements_by_css_selector('.p-quan-white')
                    snSpider.items['product_discount_sn'] = product_discount_sn
                except NoSuchElementException:
                    snSpider.items['product_discount_sn'] = 'no discount'
                yield snSpider.items
                self.driver.switch_to_window(home_page)
                print('dddd')


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
