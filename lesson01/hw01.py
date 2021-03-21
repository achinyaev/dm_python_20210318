import time
import json
from pathlib import Path
import requests


# url = "https://5ka.ru/api/v2/special_offers/"
#
# params = {
#     "records_per_page": 20,
# }
#
#
#
#
# response: requests.Response = requests.get(url, params=params)
#
# if response.status_code == 200:
#     html_file = Path(__file__).parent.joinpath('5ka.json')
#     html_file.write_text(response.text)


class Parse5ka():
    params = {
        "records_per_page": 20,
    }

    def __init__(self, start_url: str, result_path: Path, cat_id: str):
        self.start_url = start_url
        self.result_path = result_path
        if cat_id is not None:
            self.params['categories'] = int(cat_id)
            print(cat_id, self.params)

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        while True:
            print("get response", url, self.params)
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
            print('response code =', response.status_code)
            time.sleep(1)

    def run(self):
        print('start url -> ', self.start_url)
        for product in self._parse(self.start_url):
            self._save(product)

    def _parse(self, url):
        while url:
            print('URl in class ->', self.params, url)
            response = self._get_response(url, params=self.params)
            data = response.json()
            print(type(data))
            print('data - > ', data)
            url = data.get("next")
            for product in data.get("results", []):
                print('product - >',product)
                yield product

    def _save(self, data):
        file_path = self.result_path.joinpath(f'{data["id"]}.json')
        file_path.write_text(json.dumps(data, ensure_ascii=False))


if __name__ == "__main__":
    file_path = Path(__file__).parent.joinpath("categories")
    if not file_path.exists():
        file_path.mkdir()
    print(file_path)
    #parser = Parse5ka("https://5ka.ru/api/v2/special_offers/", file_path)
    #parser.run()
    parser = Parse5ka("https://5ka.ru/api/v2/special_offers/", file_path, None)
    url = "https://5ka.ru/api/v2/special_offers/"
    url_cat = "https://5ka.ru/api/v2/categories/"
    response = requests.get(url_cat)
    data_parent = response.json()
    #print(type(data))
    for parent_group_code in data_parent: #parent_group_code
        print(parent_group_code)
        print(parent_group_code.get('parent_group_code'))
        cat_path = file_path.joinpath(parent_group_code.get('parent_group_code'))
        print(cat_path)
        if not cat_path.exists():
            cat_path.mkdir()
        url_parent = url_cat + parent_group_code.get('parent_group_code') + '/'
        print(f'Parent {url_parent}')
        response = requests.get(url_parent)
        data_group = response.json()
        print('data_group >',data_group)
        for group_code in data_group:
            print('не понятка -> ',group_code.get('group_code'))
            url_group = url + group_code.get('group_code') + '/'
            print(f'Parent {url_group}')
            group_path = cat_path.joinpath(group_code.get('group_code'))
            print('Finish path ->', group_path)
            if not group_path.exists():
                group_path.mkdir()
            print('Parser',url_group, group_path)
            parser = Parse5ka(url, group_path, group_code.get('group_code'))
            parser.run()


    #print(data.get('parent_group_code',[]))
    #print(data[0])