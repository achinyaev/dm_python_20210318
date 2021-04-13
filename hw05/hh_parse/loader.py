import re

from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose


def flat_text(items):
    return "".join(items)

def salary_list(items):
    ll = []
    for x in [x.replace('\xa0','') for x in items]:
        if x.isdigit():
            ll.append(x)
    return ll if ll.__len__() > 0 else items

def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)

def desc_text(items):
    return "\n".join(items)

def tag_list(items):

    return items

def sphere_list(items):
    return items[0].split(',')

class HeadhunterLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    desc_out = desc_text
    tag_out = tag_list
    # author_in = MapCompose(hh_user_url)
    # author_out = TakeFirst()
    empl_title_out = TakeFirst()
    empl_website_out = TakeFirst()
    empl_desc_out = desc_text
    empl_sphere_out = sphere_list

