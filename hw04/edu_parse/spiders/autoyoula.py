import scrapy
import pymongo
import re
import datetime


class AutoyoulaSpider(scrapy.Spider):
    name = 'autoyoula'
    allowed_domains = ['auto.youla.ru']
    start_urls = ['https://auto.youla.ru/']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dbclient = pymongo.MongoClient()

    @staticmethod
    def get_author_id(response):
        marker = "window.transitState = decodeURIComponent"
        for script in response.css("script"):
            try:
                if marker in script.css("::text").extract_first():
                    re_pattern = re.compile(r"youlaId%22%2C%22([a-zA-Z|\d]+)%22%2C%22avatar")
                    result = re.findall(re_pattern, script.css("::text").extract_first())
                    return (
                        response.urljoin(f"/user/{result[0]}").replace("auto.", "", 1)
                        if result
                        else None
                    )
            except TypeError:
                pass

    def parse(self, response):
        brands = response.css("div.TransportMainFilters_brandsList__2tIkv a.blackLink")
        for brand in brands:
            url = brand.attrib['href']
            yield response.follow(url, callback=self.brand_parse)

    def _get_follow(self, response, select_str, callback, **kwargs):
        for a in response.css(select_str):
            #url = a.attrib.get("href")
            url = a.attrib["href"]
            yield response.follow(url, callback=callback, **kwargs)


    def brand_parse(self, response):
        #tt = response
        ##print(1)
        #print(f'url cars = {tt.attrib["url"]}')
        yield from \
            self._get_follow(response, "div.TransportMainFilters_brandsList__2tIkv a.blackLink", self.brand_parse)

        yield from \
            self._get_follow(response, "article.SerpSnippet_snippet__3O1t2 a.SerpSnippet_name__3F7Yu", self.car_parse,)

    def car_parse(self, response):
        try:
            data = {
                "title": response.css("div.AdvertCard_advertTitle__1S1Ak::text").extract_first(),
                "seller": AutoyoulaSpider.get_author_id(response),
                "price": float(response.css("div.AdvertCard_price__3dDCr::text").extract_first().replace("\u2009", "")),
                "photo_url": response.css("img.PhotoGallery_photoImage__2mHGn::attr(src)").extract(),
                "specification": [],
                "description": response.css("div.AdvertCard_descriptionInner__KnuRi::text").extract_first(),
                "phone": response.css("div.PopupPhoneNumber_block__nF2xR span.PopupPhoneNumber_number__1hybY::text").extract_first(),
                "url": response.url
            }
            for items in response.css("div.AdvertSpecs_row__ljPcX"):
                div_data = items.css("div.AdvertSpecs_data__xK2Qx::text").extract_first()
                data["specification"].append({
                    "name": items.css("div.AdvertSpecs_label__2JHnS::text").extract_first(),
                    "value": div_data if div_data else items.css("div.AdvertSpecs_data__xK2Qx a::text").extract_first()
                })
            self.dbclient[self.name+datetime.datetime].insert_one(data)

        except (AttributeError, ValueError):
            pass



