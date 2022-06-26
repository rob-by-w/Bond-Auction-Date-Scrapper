import requests
from bs4 import BeautifulSoup
from http import HTTPStatus


def get_page(page_url):
    page = requests.get(page_url)
    if page.status_code == HTTPStatus.OK:
        page_html = BeautifulSoup(page.text, "html.parser")

        return [page.status_code, page_html]

    return [page.status_code, None]
