import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def parse(self, response):
        print(1)

    def brand_parse(self, response):
        brands = response.css("")