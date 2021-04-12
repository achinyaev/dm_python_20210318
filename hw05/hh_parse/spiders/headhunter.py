import scrapy

from hw05.hh_parse.spiders.xpaths import HH_PAGE_XPATH, HH_VAC_XPATH

## смотреть 57 минута и 1ч 10 мин, внимательно разберись с сылками и переходами

class HeadhunterSpider(scrapy.Spider):
    name = 'headhunter'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?schedule=remote&L_profession_id=0&area=113']

    def parse(self, response):
        # callbacks = {"pagination": self.parse, "vacancy": self.vacancy_parse}
        # yield from self._get_follow_xpath(
        #     response, self.
        # )
        # aa = response.xpath("//div[contains(@class, 'vacancy-serp-item_premium')]//a[@class='bloko-link'][contains(@href,'vacancy')]/@href").extract()
        yield from self._get_follow_xpath(response,
                                          "//div[contains(@class, 'vacancy-serp-item_premium')]//a[@class='bloko-link'][contains(@href,'vacancy')]/@href",
                                          self.vacancy_parse)

        #print(1)
        #pass

    def _get_follow_xpath(self, response, selector, callback, **kwargs):
        for url in response.xpath(selector):
            yield response.follow(url, callback=callback, cb_kwargs=kwargs)
        print(1)
        pass
        # for url in response.xpath(xpath):
        #     yield response.follow(url, callback=callback)

    def vacancy_parse(self, response):
        print(1)
        pass
    #     loader = HHLoader(response=response)
    #     loader.add_value("url", response.url)
    #     for key, xpath in HH_VACANCY_XPATH.items():
    #         loader.add_xpath(key, xpath)
    #
    #     yield loader.load_item()

    def company_parse(self, response):
        pass
