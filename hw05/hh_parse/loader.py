import re

from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose


def clear_price(price: str) -> float:
    pass
    # try:
    #     result = float(price.replace("\u2009", ""))
    # except ValueError:
    #     result = None
    # return result

def get_characteristics(item: str) -> dict:
    pass
    # selector = Selector(text=item)
    # data = {
    #     "name": selector.xpath("//div[contains(@class, 'AdvertSpecs')]/text()").extract_first(),
    #     "value": selector.xpath(
    #         "//div[contains(@class, 'AdvertSpecs_data')]//text()"
    #     ).extract_first(),
    # }
    # return data

def get_author_id(text):
    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
    result = re.findall(re_pattern, text)
    try:
        user_link = f"https://youla.ru/user/{result[0]}"
    except IndexError:
        user_link = ""
    return user_link

class AutoyoulaLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    price_in = MapCompose(clear_price)
    price_out = TakeFirst()
    characteristics_in = MapCompose(get_characteristics)
    description_out = TakeFirst()
    author_in = MapCompose(get_author_id)
    author_out = TakeFirst()


def flat_text(items):
    return "".join(items)

def salary_list(items):
    ll = []
    for x in [x.replace('\xa0','') for x in items]:
        if x.isdigit():
            ll.append(x)
    return ll if ll.__len__() > 0 else items

def hh_user_url(user_id):
    # print(1)
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

