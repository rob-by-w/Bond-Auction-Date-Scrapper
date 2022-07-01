import io
from http import HTTPStatus

import requests
from bs4 import BeautifulSoup
from tabula.io import read_pdf


def get_page_html(page_url):
    page = requests.get(page_url)
    if page.status_code == HTTPStatus.OK:
        page_html = BeautifulSoup(page.text, "html.parser")

        return [page.status_code, page_html]

    return [page.status_code, None]


def get_page_df(page_url):
    page = requests.get(page_url)

    if page.status_code == HTTPStatus.OK:
        memory_file = io.BytesIO(page.content)
        page_df = read_pdf(memory_file, pages="all")

        return [page.status_code, page_df]

    return [page.status_code, None]
