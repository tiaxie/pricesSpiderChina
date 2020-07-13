from __future__ import absolute_import
import pathlib
import scrapy
from scrapy import spiderloader
from scrapy.utils import project
from scrapy.utils.project import get_project_settings
from twisted import runner
from twisted.internet.defer import inlineCallbacks
from multiprocessing import Process
from tmallspider.items import TmallspiderItem
from tmallspider.items import JdspiderItem
from tmallspider.items import SnspiderItem
from tmallspider.items import DdspiderItem
from scrapy.utils.response import open_in_browser
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

class tmallSpider(scrapy.Spider):

    name = 'tspider'
    start_urls = [
        'https://list.tmall.com/search_product.htm?q={}'.format('ipad')
    ]

    def parse(self, response):
        open_in_browser(response)
        items = TmallspiderItem()
        product_info = response.css('.product-iWrap')

        for product in product_info:
            product_name_tmall = product.css('.productTitle a').xpath('normalize-space(.)').get()
            product_price_tmall = product.css('.productPrice em::text').extract()
            items['product_name_tmall'] = product_name_tmall
            items['product_price_tmall'] = product_price_tmall
            yield items

class jdSpider(scrapy.Spider):

    name = 'jspider'
    start_urls = [
        'https://search.jd.com/Search?keyword={}'.format('iPad air3')
    ]

    def parse(self, response):
        #open_in_browser(response)
        items = JdspiderItem()
        product_info = response.css('.gl-i-wrap')

        for product in product_info:
            product_name_jd = product.css('.p-name-type-2 em').xpath('normalize-space(.)').get()
            product_price_jd = product.css('.p-price i').xpath('normalize-space(.)').get()
            items['product_name_jd'] = product_name_jd
            items['product_price_jd'] = product_price_jd
            yield items

class ddSpider(scrapy.Spider):
    name = 'dspider'
    start_urls = [
        'http://search.dangdang.com/?key={}&act=input'.format('iPad air 3')
    ]

    def parse(self, response):
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
    start_urls = [
        'http://search.suning.com/{}/'.format('iPad air 3')
    ]

    def parse(self, response):
        #open_in_browser(response)
        product_info = response.css('.item-bg')
        for product in product_info:
            product_link = 'http:'+product.css('a::attr(href)')[0].extract()
            yield scrapy.Request(product_link, callback=self.start_scraping)

    def start_scraping(self, response):
        #open_in_browser(response)
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

