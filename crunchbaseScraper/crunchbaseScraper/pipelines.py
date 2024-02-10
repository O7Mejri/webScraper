# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CrunchbasescraperPipeline:
    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        # custom data cleaning and processing functions
        
        return item


import psycopg2
from scrapy.exceptions import NotConfigured

class SaveDataPipeline:
    def __init__(self, database_settings):
        self.database_settings = database_settings
        self.conn = None
        self.cur = None

    @classmethod
    def from_crawler(cls, crawler):
        database_settings = crawler.settings.getdict('DATABASE')
        if not database_settings:
            raise NotConfigured("DATABASE settings is not configured")
        return cls(database_settings)

    def open_spider(self, spider):
        self.conn = psycopg2.connect(**self.database_settings)
        self.cur = self.conn.cursor()
        self.create_table()

    def close_spider(self, spider):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def create_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                company_name TEXT,
                industry TEXT,
                location TEXT
            )
        """
        self.cur.execute(sql)
        self.conn.commit()

    def process_item(self, item, spider):
        sql = """
            INSERT INTO companies (company_name, industry, location)
            VALUES (%s, %s, %s)
        """
        self.cur.execute(sql, (
            item['company_name'],
            item['industry'],
            item['location']
        ))
        self.conn.commit()
        return item
