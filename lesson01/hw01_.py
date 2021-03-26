import time
import json
from pathlib import Path
import requests

class Parse5ka():
    params = {
        "records_per_page": 20,
    }

    def __init__(self, start_url: str, result_path: Path, cat_id: str):
        self.start_url = start_url
        self.result_path = result_path
        if cat_id is not None:
            self.params['categories'] = int(cat_id)

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            time.sleep(1)

    def run(self):
        for product in self._parse(self.start_url):
            self._save(product)

    def _parse(self, url):
        while url:
            response = self._get_response(url, params=self.params)
            data = response.json()
            url = data.get("next")
            for product in data.get("results", []):
                yield product

    def _save(self, data):
        file_path = self.result_path.joinpath(f'{data["id"]}.json')
        file_path.write_text(json.dumps(data, ensure_ascii=False))

class CatParser(Parse5ka):
    def __init__(self, cat_url:  *args, **kwargs):
        self.cat_url = cat_url
        super().__init__(*args, **kwargs)

    def _get_cat(self):
        response = requests.get(self.cat_url)
        if response.status_code == 200:
            return response.json()

    def run(self):
        data = self._get_cat()
        for categories in data:
            


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("categories")
    if not file_path.exists():
        file_path.mkdir()
    parser = Parse5ka("https://5ka.ru/api/v2/special_offers/", file_path, None)
    url = "https://5ka.ru/api/v2/special_offers/"
    url_cat = "https://5ka.ru/api/v2/categories/"
    response = requests.get(url_cat)
    data_parent = response.json()
    for parent_group_code in data_parent: #parent_group_code
        cat_path = file_path.joinpath(parent_group_code.get('parent_group_code'))
        if not cat_path.exists():
            cat_path.mkdir()
        url_parent = url_cat + parent_group_code.get('parent_group_code') + '/'
        response = requests.get(url_parent)
        data_group = response.json()
        for group_code in data_group:
            url_group = url + group_code.get('group_code') + '/'
            group_path = cat_path.joinpath(group_code.get('group_code'))
            if not group_path.exists():
                group_path.mkdir()
            parser = Parse5ka(url, group_path, group_code.get('group_code'))
            parser.run()

