import time
import json
from pathlib import Path
import requests

class Parser5ka:

    def __init__(self, start_url: str, save_path: Path, *args, **kwargs ):
        self.start_url = start_url
        self.save_path = save_path
        if not self.save_path.exists():
            self.save_path.mkdir()

    def _get_response(self, url):
        while True:
            response = requests.get(url)
            if response.status_code == 200:
                return response
            time.sleep(0.5)

    def run(self):
        for product in self._parse(self.start_url):
            product_path = self.save_path.joinpath(f"{product['id']}.json")
            self._save(product, product_path)

    def _parse(self, url: str):
        while url:
            response = self._get_response(url)
            data: dict = response.json()
            url = data["next"]
            for product in data["results"]:
                yield product

    def _save(self, data: dict, file_path: Path):
        file_path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf8')

class CategoriesParser(Parser5ka):
    def __init__(self, categories_url, *args, **kwargs):
        self.categories_url = categories_url
        super().__init__(*args, **kwargs)

    def _get_categories(self):
        response = self._get_response(self.categories_url)
        data = response.json()
        return data

    def run(self):
        for category in self._get_categories():
            category["products"] = []
            params = f"?categories={category['parent_group_code']}"
            url = f"{self.start_url}{params}"
            category["products"].extend(list(self._parse(url)))
            file_name = f"{category['parent_group_code']}-{category['parent_group_name']}.json"
            cat_path = self.save_path.joinpath(file_name)
            self._save(category, cat_path)


def gen_save_path(dir_name):
    save_path = Path(__file__).parent.joinpath(dir_name)
    return save_path

if __name__ == "__main__":
    url = "https://5ka.ru/api/v2/special_offers/"
    cat_url = "https://5ka.ru/api/v2/categories/"
    save_path_categories = gen_save_path("categories")
    cat_parser = CategoriesParser(cat_url, url, save_path_categories)
    cat_parser.run()