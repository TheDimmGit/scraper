# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SdScraperItem(scrapy.Item):
    name = scrapy.Field()
    rating = scrapy.Field()
    reviews = scrapy.Field()
    yelp_url = scrapy.Field()
    url = scrapy.Field()
    review_info = scrapy.Field()
