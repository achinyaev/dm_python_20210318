import scrapy
import pymongo

from hw05.hh_parse.spiders.xpaths import HH_EMPL_XPATH, HH_VAC_XPATH
from hw05.hh_parse.loader import HeadhunterLoader

## смотреть 57 минута и 1ч 10 мин, внимательно разберись с сылками и переходами



class HeadhunterSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    _xpath_selectors = {
        "vacancy": "//div[contains(@class, 'vacancy-serp-item_premium')]//a[@class='bloko-link'][contains(@href,'vacancy')]/@href",
        "pagination": "//div[@data-qa='pager-block']//a[@class='bloko-button'][@data-qa='pager-next'][@rel='nofollow']/@href",
        "employer_url": "//div[@class='vacancy-company-wrapper']//a[@class='vacancy-company-name']/@href",
    }

    _xpath_vacancy_selector = {
        "title": "//div[@class='vacancy-title']/h1[@class='bloko-header-1'][@data-qa='vacancy-title']"
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_client = pymongo.MongoClient()

    def parse(self, response):
        yield from self._get_follow_xpath(response, self._xpath_selectors["pagination"], self.parse)
        yield from self._get_follow_xpath(response, self._xpath_selectors["vacancy"],  self.vacancy_parse)


    def _get_follow_xpath(self, response, selector, callback, **kwargs): #
        for url in response.xpath(selector):
            yield response.follow(url, callback=callback, cb_kwargs=kwargs)

    def vacancy_parse(self, response):
        loader = HeadhunterLoader(response=response)
        loader.add_value("url", response.url)
        # print(f'process --> {response.url}')
        for key, xpath in HH_VAC_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
        yield from self._get_follow_xpath(response, self._xpath_selectors["employer_url"],  self.employer_parse)
        #self.db_client["hh_parse_20210410"][self.name].insert_one(loader._values)

    def employer_parse(self, response):
        loader = HeadhunterLoader(response=response)
        loader.add_value("url", response.url)
        # print(f'process --> {response.url}')
        for key, xpath in HH_EMPL_XPATH.items():
            loader.add_xpath(key, xpath)
        yield loader.load_item()
