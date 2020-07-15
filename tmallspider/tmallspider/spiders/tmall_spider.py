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

def encodeGB2312(data):
    hexData = data.encode(encoding='GB2312').hex().upper()
    encoded = '%' + '%'.join(hexData[i:i + 2] for i in range(0, len(hexData), 2))
    return encoded

class tmallSpider(scrapy.Spider):

    name = 'tspider'
    output = encodeGB2312('iPad air 3')
    start_urls = [
        'https://list.tmall.com/search_product.htm?q={}'.format(output)
    ]

    items = TmallspiderItem()

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path = '/usr/bin/chromedriver')

    def parse(self, response):
        #open_in_browser(response)
        product_info = response.css('.product-iWrap')
        for product in product_info:
            product_name_tmall = product.css('.productTitle a').xpath('normalize-space(.)').get()
            product_price_tmall = product.css('.productPrice em::text').extract()
            tmallSpider.items['product_name_tmall'] = product_name_tmall
            tmallSpider.items['product_price_tmall'] = product_price_tmall
            product_detail_link = 'http:' + product.css('a::attr(href)')[0].extract()
            yield scrapy.Request(product_detail_link, callback=self.start_scraping)

    def start_scraping(self, response):
        self.driver.get(response.url)
        self.driver.switch_to.frame(self.driver.find_element_by_id('sufei-dialog-content'))
        self.driver.find_element_by_id('fm-login-id').send_keys('iamgooglepenn')
        self.driver.find_element_by_id('fm-login-password').send_keys('Hello_World2019')
        self.time.sleep(5)
        self.driver.find_element_by_css_selector('.fm-button.fm-submit.password-login').click()
        discount = self.driver.find_element_by_css_selector('.tm-gold dd')
        #discount = response.css('.tm-gold dd').extract()
        tmallSpider.items['product_discount_tmall'] = discount
        yield tmallSpider.items

class jdSpider(scrapy.Spider):

    name = 'jspider'
    keyword ='ipad air 3'
    start_urls = [
        'https://search.jd.com/Search?{url_suffix}'.format(url_suffix=urllib.parse.urlencode({'keyword': keyword}, encoding='utf-8'))
    ]
    items = JdspiderItem()
    def parse(self, response):
        open_in_browser(response)
        product_info = response.css('.gl-i-wrap')
        product = product_info[0]

        for product in product_info:
            product_name_jd = product.css('.p-name-type-2 em').xpath('normalize-space(.)').get()
            product_price_jd = product.css('.p-price i').xpath('normalize-space(.)').get()
            jdSpider.items['product_name_jd'] = product_name_jd
            jdSpider.items['product_price_jd'] = product_price_jd
            
            product_detail_link = 'http:'+product.css('a::attr(href)')[0].extract()
            yield scrapy.Request(product_detail_link, callback=self.start_scraping)

    def start_scraping(self, response):
        #open_in_browser(response)
        product_discount_jd = response.css('#summary-quan .text').extract()
        jdSpider.items['product_discount_jd'] = product_discount_jd
        yield jdSpider.items

class ddSpider(scrapy.Spider):
    name = 'dspider'
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
    name = 'sspider'
    keyword = 'ipad air 3 64G'
    start_urls = [
        'https://search.suning.com/{}/'.format('iPad air 3')
        #'https://search.suning.com/{url_suffix}/'.format(url_suffix=urllib.parse.urlencode({'keyword': keyword}, encoding='utf-8'))
    ]

    def parse(self, response):
        #open_in_browser(response)
        product_info = response.css('.item-bg')
        for product in product_info:
            product_link = 'http:'+product.css('a::attr(href)')[0].extract()
            yield scrapy.Request(product_link, callback=self.start_scraping)

    def start_scraping(self, response):
        #open_in_browser(response) DO NOT UNCOMMENT
        items = SnspiderItem()
        items['product_name_sn'] = response.css('#itemDisplayName').xpath('normalize-space(.)').get()
        items['product_price_sn'] = response.css('.mainprice').extract()
        yield items

'''
process = CrawlerProcess(settings={
    "FEEDS": {
        "tmallitem.csv": {"format": "csv", 'fields': ['product_name_tmall', 'product_price_tmall'],},
        "jditem.csv": {"format": "csv", 'fields': ['product_name_jd', 'product_price_jd'],},
        "snitem.csv": {"format": "csv", 'fields': ['product_name_sn', 'product_price_sn'],},
        "dditem.csv": {"format": "csv", 'fields': ['product_name_dd', 'product_price_dd'],},
    },
})

process.crawl(tmallSpider)
process.crawl(jdSpider)
process.crawl(snSpider)
process.crawl(ddSpider)
process.start()
'''

