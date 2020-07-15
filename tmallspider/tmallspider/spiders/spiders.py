from __future__ import absolute_import
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import scrapy
from tmallspider.items import TmallspiderItem
from tmallspider.items import JdspiderItem
from tmallspider.items import SnspiderItem
from tmallspider.items import DdspiderItem
from scrapy.utils.response import open_in_browser
from scrapy.crawler import CrawlerRunner, CrawlerProcess
import urllib.parse
from selenium.webdriver.support.ui import WebDriverWait

class tmallSpider(scrapy.Spider):
    name = 'ttspider'
    output = 'iPad'
    start_urls = [
        'http://login.tmall.com'
    ]
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        self.driver.get(response.url)
        self.driver.switch_to.frame(self.driver.find_element_by_id('J_loginIframe'))
        self.driver.find_element_by_name('fm-login-id').send_keys('iamgooglepenn')
        self.driver.find_element_by_id('fm-login-password').send_keys('Hello_World2019')
        self.driver.find_element_by_class_name('fm-button fm-submit password-login').click()