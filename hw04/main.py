from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from edu_parse.spiders.autoyoula import AutoyoulaSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule("edu_parse.settings")
    crawler_proc= CrawlerProcess(settings=crawler_settings)
    crawler_proc.crawl(AutoyoulaSpider)
    crawler_proc.start()
    pass
