from hh_parse.spiders.headhunter import HeadhunterSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
	crawler_settings = Settings()
	crawler_settings.setmodule("hh_parse.settings")
	crawler_proc = CrawlerProcess(settings=crawler_settings)
	crawler_proc.crawl(HeadhunterSpider)
	crawler_proc.start()
