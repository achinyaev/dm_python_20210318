import scrapy


class HeadhunterSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response):
        print(1)
        pass
