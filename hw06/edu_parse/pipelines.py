# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline

from scrapy import Request
import pymongo

class EduParsePipeline:
    def process_item(self, item, spider):
        return item

class EduParseMongoPipeline:
    def __init__(self):
        client = pymongo.MongoClient()
        self.db = client["avito"]

    def process_item(self, item, spider):
        self.db[spider.name].insert_one(item)
        return item

class EduImageDownloadPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for url in item.get("photos", []):
            yield Request(url)

    def item_completed(self, results, item, info):
        if "photos" in item:
            item["photos"] = [itm[1] for itm in results]
        return item