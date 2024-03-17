# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class BookScrapyItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    description = scrapy.Field()
    pages = scrapy.Field()
    publish_year = scrapy.Field()
    language = scrapy.Field()
    rating = scrapy.Field()
    genres = scrapy.Field()
    review_counts = scrapy.Field()
    source = scrapy.Field()
