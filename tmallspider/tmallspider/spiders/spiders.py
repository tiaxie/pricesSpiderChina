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

class tmallSpider(scrapy.Spider):
    name = 'ttspider'
    output = 'iPad'
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
        self.driver.find_element_by_class_name('fm-btn').click()
        #fm-button fm-submit password-login
        time.sleep(2)
        self.driver.find_element_by_name('q').send_keys('iPad')
        time.sleep(2)
        self.driver.find_element_by_css_selector('button').click()
        n = 0
        #yanzheng = 0
        for element in WebDriverWait(self.driver, 30).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '.product-iWrap'))):
            if n < 2:
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
                #new

                element.click()
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
                self.driver.get(response.url)
                time.sleep(2)
                #self.driver.switch_to(self.driver.window_handles[n])
                try:
                    time.sleep(2)
                    product_disount_tmall = self.driver.find_element_by_css_selector('.tm-price').text
                    tmallSpider.items['product_discount_tmall'] = product_disount_tmall
                except NoSuchElementException:
                    tmallSpider.items['product_discount_tmall'] = 'no discount'
                self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
                yield tmallSpider.items
                #new


