# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TmallspiderItem(scrapy.Item):
    # define the fields for your item here like:
    product_name_tmall = scrapy.Field()
    product_price_tmall = scrapy.Field()

class JdspiderItem(scrapy.Item):
    product_name_jd = scrapy.Field()
    product_price_jd = scrapy.Field()

class SnspiderItem(scrapy.Item):
    product_name_sn = scrapy.Field()
    product_price_sn = scrapy.Field()

class DdspiderItem(scrapy.Item):
    product_name_dd = scrapy.Field()
    product_price_dd = scrapy.Field()


