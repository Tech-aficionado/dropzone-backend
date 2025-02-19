import scrapy
from scrapy.exceptions import CloseSpider
import random
import time
import asyncio
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sqlite3
from datetime import datetime

class MultiVendorProductSpider(scrapy.Spider):
    name = "multi_vendor_products"

    def __init__(self, max_products=100, *args, **kwargs):
        super(MultiVendorProductSpider, self).__init__(*args, **kwargs)
        self.max_products = int(max_products)
        self.product_count = 0
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        ]
        self.db_conn = sqlite3.connect('product_prices.db')
        self.create_table()

    def create_table(self):
        cursor = self.db_conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS product_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            mrp REAL,
            vendor TEXT,
            timestamp DATETIME
        )
        ''')
        self.db_conn.commit()

    def start_requests(self):
        vendors = {
            'amazon': 'https://www.amazon.in/s?k={}',
            # Add more vendors here
        }
        keywords = ["oneplus 13"]  # Add more keywords as needed
        
        for vendor, url_template in vendors.items():
            for keyword in keywords:
                url = url_template.format(keyword.replace(" ", "+"))
                yield scrapy.Request(
                    url,
                    callback=self.parse_search_results,
                    headers=self.get_headers(),
                    meta={'vendor': vendor, 'keyword': keyword}
                )

    def get_headers(self):
        return {
            "User-Agent": random.choice(self.user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
        }

    def parse_search_results(self, response):
        vendor = response.meta['vendor']
        if vendor == 'amazon':
            products = response.css('div[data-asin]:not([data-asin=""])')
            for product in products:
                if self.product_count >= self.max_products:
                    raise CloseSpider("Reached maximum number of products")
                asin = product.attrib["data-asin"]
                product_url = f"https://www.amazon.in/dp/{asin}"
                yield scrapy.Request(
                    product_url,
                    callback=self.parse_product_page,
                    headers=self.get_headers(),
                    meta={'dont_retry': True, 'vendor': vendor}
                )
                self.product_count += 1
        elif vendor == 'flipkart':
            # Implement Flipkart-specific parsing logic here
            pass
        # Add more vendor-specific parsing logic as needed

        # Pagination logic (example for Amazon)
        if vendor == 'amazon' and self.product_count < self.max_products:
            next_page = response.css("a.s-pagination-next::attr(href)").get()
            if next_page:
                yield response.follow(
                    next_page,
                    callback=self.parse_search_results,
                    headers=self.get_headers(),
                    meta=response.meta
                )

    def parse_product_page(self, response):
        vendor = response.meta['vendor']
        if vendor == 'amazon':
            name = response.css("#productTitle::text").get().strip()
            price = response.css(".a-price-whole::text").get()
            mrp = response.css(".a-text-price .a-offscreen::text").get()
        elif vendor == 'flipkart':
            # Implement Flipkart-specific parsing logic here
            pass
        # Add more vendor-specific parsing logic as needed

        item = {
            "name": name,
            "price": price,
            "mrp": mrp,
            "vendor": vendor,
            "timestamp": datetime.now().isoformat()
        }
        
        self.save_to_db(item)
        yield item

    def save_to_db(self, item):
        cursor = self.db_conn.cursor()
        cursor.execute('''
        INSERT INTO product_prices (name, price, mrp, vendor, timestamp)
        VALUES (?, ?, ?, ?, ?)
        ''', (item['name'], item['price'], item['mrp'], item['vendor'], item['timestamp']))
        self.db_conn.commit()

    def closed(self, reason):
        self.db_conn.close()

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

# Run the spider
if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl(MultiVendorProductSpider)
    process.start()
