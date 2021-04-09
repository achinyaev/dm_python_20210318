import scrapy


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def parse(self, response):
        brands = response.css("div.TransportMainFilters_brandsList__2tIkv a.blackLink")
        for brand in brands:
            url = brand.attrib['href']
            yield response.follow(url, callback=self.brand_parse)

    def brand_parse(self, response):
        tt = response
        print(1)
        #print(f'url cars = {tt.attrib["url"]}')
