from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from gd_parse.spiders.autoyoula import AutoyoulaSpider

if __name__ == '__main__':
    crawler_setting = Settings()
    crawler_setting.setmodule("gd_parse.settings")
    crawler_proc = CrawlerProcess(settings=crawler_setting)
    crawler_proc.crawl(AutoyoulaSpider)
    crawler_proc.start()
