import typing
import requests
import bs4
from urllib.parse import urljoin
from db import Database


class GbBlogParse:
    def __init__(self, start_url, database: Database):
        self.start_url = start_url
        self.db = database
        self.done_urls = set()
        self.tasks = [
            self.get_task(self.start_url, self.parse_feed),
        ]

    def get_task(self, url: str, callback: typing.Callable) -> typing.Callable:
        def task():
            soup = self._get_soup(url)
            return callback(url, soup)
        return task()

    def _get_response(self, url, *args, **kwargs) -> requests.Response:
        # обработать статус коды и ошибки
        for _ in range(10):
            response = requests.get(url, *args, **kwargs)
            if response.status_code == 200:
                return response
        raise ValueError("Error URL")

    def _get_soup(self, url, *args, **kwargs):
        soup = bs4.BeautifulSoup(self._get_response(url, *args, **kwargs), "lxml")
        return soup

    def parse_post(self, url, soup):
        pass

    def parse_feed(self, url, soup):
        pass

    def save(self, data):
        self.db.create_post(data)


    def run(self):
        #task = self.get_task(self.start_url, self.parse_feed)
        #self.tasks.append(task)
        #self.done_urls.add(self.start_url)
        for task in self.tasks:
            task_result = task()
            if task_result:
                self.db.create_post(task_result)



if __name__ == '__main__':
    database = Database("sqlite:///gb_blog.db")
    parser = GbBlogParse("https://geekbrains.ru/posts")
    parser.run()




