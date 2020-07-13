# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

#conn = sqlite3.connect('prices.db')
#curr = conn.cursor()
#curr.execute("""create table price_tb(
#                product_name text,
#                product_price text
#                )""")
#conn.commit()
#conn.close()
class TmallspiderPipeline(object):

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect("prices.db")
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS  price_tb""")
        self.curr.execute("""create table price_tb(
                                product_name text,
                                product_price_tmall text
                                )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into price_tb values(?,?,?)""", (
            item['product_name'][0],
            item['product_price_tmall'][0]
        ))
        self.conn.commit()
