import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from crunchbaseScraper.items import CrunchbaseCompanyItem

class CrunchbaseSpider(CrawlSpider):
    name = 'crunchbase_scraper'
    allowed_domains = ['crunchbase.com']
    start_urls = ['https://www.crunchbase.com/discover/organization.companies/4ec4eab64c08463791a991ce56b5e8b0']

    rules = (
        Rule(LinkExtractor(allow=r'/organization/[^/]+$'), callback='parse_company', follow=True),
    )
    # custom header
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0",
    }

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, headers=self.HEADERS, callback=self.parse)

    def parse_company(self, response):
        if response.status == 403:
            self.logger.warning("Forbidden response received for URL: %s", response.url)
            return

        item = CrunchbaseCompanyItem()
        item['company_name'] = response.css('h1[data-test="profile-name"]::text').get()
        item['industry'] = response.css('a[data-test="profile-industry"]::text').get()
        item['location'] = response.css('span[data-test="location-and-type"]::text').get()

        yield item

        if len(self.crawler.stats.get_value('item_scraped_count', 0)) >= 20:
            self.crawler.engine.close_spider(self, 'Scraped 20 companies')

    def closed(self, reason):
        self.logger.info('Spider closed: %s', reason)
