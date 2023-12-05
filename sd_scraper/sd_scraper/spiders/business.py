
import scrapy

from sd_scraper.items import SdScraperItem
from urllib.parse import unquote


NUMBER_OF_PAGES = 230   # 230 stands for 24th page, 0 for first


class BusinessSpider(scrapy.Spider):
    name = "business"
    allowed_domains = ["yelp.com"]

    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'output.json'
    }

    def start_requests(self):
        base_url = "https://www.yelp.com/search?find_desc=Contractors&find_loc=San%20Francisco%2C%20CA&start={}"

        for start_page in range(0, NUMBER_OF_PAGES, 10):
            yield scrapy.Request(url=base_url.format(start_page), callback=self.parse)

    def parse(self, response):
        all_b = response.css('div.mainAttributes__09f24__bQYNE')
        for b in all_b:
            item = SdScraperItem()

            name = b.css('span.css-1egxyvc a::attr(name)').get()
            item['name'] = name

            rating = b.css('span.css-gutk1c::text').get()
            item['rating'] = rating

            review = b.css('span.css-8xcil9::text').get()
            if review:
                reviews_number = int(b.css('span.css-8xcil9::text').get().split()[0].lstrip('('))
                item['reviews'] = reviews_number
            else:
                item['reviews'] = 0

            yelp_link = b.css('span.css-1egxyvc a::attr(href)').get()
            full_yelp_link = f'https://www.yelp.com/{yelp_link}'
            item['yelp_url'] = f'https://www.yelp.com/{yelp_link}'

            yield scrapy.Request(url=full_yelp_link, callback=self.parse_nested_link, meta={'item': item})

    def parse_nested_link  (self, response):
        item = response.meta['item']
        business_web = response.css('div.css-s81j3n a::attr(href)').get()
        if business_web:
            try:
                url_param = business_web.split('url=')[1].split('&')[0]
                decoded_url = unquote(url_param)
                item['url'] = decoded_url
            except IndexError:
                item['url'] = None
        else:
            item['url'] = None

        reviewer_name = response.css('div.user-passport-info a::text').get()
        reviewer_loc = response.css('div.user-passport-info div div span::text').get()
        date = response.css('span.css-chan6m::text').get()
        review_info = {
            'name': reviewer_name,
            'location': reviewer_loc,
            'date': date,
        }
        item['review_info'] = review_info

        return item
