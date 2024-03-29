import re
from urllib.parse import urljoin

from scrapy.loader import ItemLoader
from scrapy import Selector
from itemloaders.processors import TakeFirst, MapCompose


def clear_price(price: str) -> float:
    try:
        result = float(price.replace("\u2009", ""))
    except ValueError:
        result = None
    return result


def get_characteristics(item: str) -> dict:
    selector = Selector(text=item)
    data = {
        "name": selector.xpath("//div[contains(@class, 'AdvertSpecs')]/text()").extract_first(),
        "value": selector.xpath(
            "//div[contains(@class, 'AdvertSpecs_data')]//text()"
        ).extract_first(),
    }
    return data


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
    return "\n".join(items)


def hh_user_url(user_id):
    return urljoin("https://hh.ru/", user_id)


class HHLoader(ItemLoader):
    default_item_class = dict
    url_out = TakeFirst()
    title_out = TakeFirst()
    salary_out = flat_text
    # description_in = flat_text,
    # description_out = flat_text,
    author_in = MapCompose(hh_user_url)
    author_out = TakeFirst()
