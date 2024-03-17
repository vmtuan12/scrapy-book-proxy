from book_scrapy.spiders.base_spider import BaseSpider
import scrapy

class ThrillerSpider(BaseSpider):

    name = 'thriller'

    def start_requests(self):
        start_url = self.start_list[self.name]
        yield scrapy.Request(url=start_url, 
                                callback=self.parse_link)