import requests


class Parser:
    def __init__(self, url):
        self.response = requests.get(url)

    def get_status(self):
        return self.response.status_code
