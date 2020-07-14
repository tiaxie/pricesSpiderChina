'''
"FEEDS": {
        "item.csv": {"format": "csv"},
    },

这段代码可以实现点进去 但点进去后 如果不选容量 颜色等细节 则不会自动显示价格
class tmallSpider(scrapy.Spider):
    name = 'tspider'
    start_urls = [
        'https://list.tmall.com/search_product.htm?q={}'.format('ipad air3')
    ]

    def parse(self, response):
        product_info = response.css('.product-iWrap')
        for product in product_info:
            product_detail_link = 'http:'+product.css('a::attr(href)')[0].extract()
            yield scrapy.Request(product_detail_link, callback=self.start_scraping)

    def start_scraping(self, response):
        items = TmallspiderItem()

'''