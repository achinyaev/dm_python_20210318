import scrapy
import pymongo
from hw06.edu_parse.spiders.xpath import AVITO_KV_XPATH, AVITO_PG_XPATH
from hw06.edu_parse.loaders import AvitoLoader

class AvitoSpider(scrapy.Spider):
    name = 'avito'
    mongo_url = "mongodb://localhost:27017"
    allowed_domains = ['www.avito.ru']
    #start_urls = ['https://www.avito.ru/krasnodar/kvartiry/prodam-ASgBAgICAUSSA8YQ?p=1']
    #start_urls = ['https://www.avito.ru/krasnodar/nedvizhimost/']
    start_urls = ['https://www.avito.ru/sankt-peterburg/kvartiry/prodam-ASgBAgICAUSSA8YQ?cd=1']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbclient = pymongo.MongoClient(self.mongo_url)
        # callbacks = {
        #     "pagination": self.parse,
        #     "kvartira": self.kv_parse,
        # }

    @staticmethod
    def _get_follow_xpath(response, xpath, callback):
        for link in response.xpath(xpath):
            yield response.follow(link, callback=callback)

    def parse(self, response, *args, **kwargs):
        callbacks = {"pagination": self.parse, "kvartira": self.kv_parse}
        for key, xpath in AVITO_PG_XPATH.items():
            yield from self._get_follow_xpath(response, xpath, self.callbacks[key])

    def kv_parse(self, response):
        self.coll_name = "kvartira"
        loader = AvitoLoader(response=response)
        loader.add_value("url", response.url)
        for key, xpath in AVITO_KV_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
