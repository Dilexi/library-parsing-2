import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup


def get_category_book_url(start_page, end_page):
    all_full_urls = []
    for number_page in range(start_page, end_page):
        tululu_url = f'https://tululu.org/l55/{number_page}'
        response = requests.get(tululu_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        books_selector = 'table.d_book'
        books_urls = soup.select(books_selector)
        for book_url in books_urls:
            url = book_url.find('a')['href']
            book_full_url = urljoin(tululu_url, url)
            all_full_urls.append(book_full_url)
    return all_full_urls
