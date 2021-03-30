import requests
import bs4
import pymongo
import time
from datetime import datetime
#from pathlib import Path
from urllib.parse import urljoin

class MagnitParse:

    date_mounth = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]

    def __init__(self, start_url, mongo_url):
        self.start_url = start_url
        client = pymongo.MongoClient(mongo_url)
        self.db = client["parse20210330_2"]

    def get_response(self, *args, **kwargs):
        for _ in range(15):
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(1)
        raise ValueError("URL DIE")


    def get_soup(self, url, *args, **kwargs) -> bs4.BeautifulSoup:
        soup = bs4.BeautifulSoup(self.get_response(url, *args, **kwargs).text, "lxml")
        return soup

    @property
    def template(self):
        data_template = {
            "url": lambda a: urljoin(self.start_url, a.attrs.get("href", "/")),
            "product_name": lambda a: a.find("div", attrs={"class": "card-sale__title"}).text,
            "image_url": lambda a: urljoin(self.start_url, a.find("picture").find("img").attrs.get("data-src", "/")),
            "date_from": lambda a: datetime(year=datetime.now().year, month=int(self.date_mounth.index(a.find("div", attrs={"class":"card-sale__date"}).text.split()[2])+1), day=int(a.find("div", attrs={"class":"card-sale__date"}).text.split()[1])),
            "date_to": lambda a: datetime(year=datetime.now().year, month=int(self.date_mounth.index(a.find("div", attrs={"class":"card-sale__date"}).text.split()[5])+1), day=int(a.find("div", attrs={"class":"card-sale__date"}).text.split()[4])),
            "promo_name": lambda a: a.find("div", attrs={"class":"card-sale__header"}).text,
            "old_price" : lambda a: float(a.find("div", attrs={"class":"label__price label__price_old"}).text.split()[0]+'.'+ a.find("div", attrs={"class":"label__price label__price_old"}).text.split()[1]) ,
            "new_price": lambda a: float(a.find("div", attrs={"class":"label__price label__price_new"}).text.split()[0]+'.'+ a.find("div", attrs={"class":"label__price label__price_new"}).text.split()[1]),
            #"old_price": float,
            #"new_price": float,


        }
        return data_template

    def run(self):
        for product in self._parse(self.get_soup(self.start_url)):
            self.save(product)

    def _parse(self, soup):
        products_a = soup.find_all("a", attrs={"class": "card-sale"})
        for prod_tag in products_a:
            product_data = {}
            for key, func in self.template.items():
                try:
                    product_data[key] = func(prod_tag)
                    print(product_data[key])
                except (AttributeError,IndexError):
                    pass
            yield product_data


    def save(self, data):
        collection = self.db["magnit"]
        collection.insert_one(data)

if __name__  == '__main__':
    url = "https://magnit.ru/promo/?geo=moskva"
    mongo_url = "mongodb://localhost:27017"
    parser = MagnitParse(url, mongo_url)
    parser.run()