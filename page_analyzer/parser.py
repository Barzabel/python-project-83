import requests
from bs4 import BeautifulSoup


class Parser:
    def __init__(self, url):
        self.response = requests.get(url)
        self.parse_data = BeautifulSoup(self.response.text, 'lxml')

    def get_data(self):
        title = self.parse_data.title.text if self.parse_data.title else None
        h1 = self.parse_data.h1.text if self.parse_data.h1 else None
        description = None
        meta = self.parse_data.find("meta", attrs={"name": "description"})
        if meta:
            description = meta.get('content', None)
        return {
            'status_code': self.response.status_code,
            'title': title,
            'h1': h1,
            'description': description,
        }
