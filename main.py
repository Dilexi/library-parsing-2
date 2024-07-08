import os
import json
import requests
import argparse
from time import sleep
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, unquote, urlsplit
from parse_tululu_category import get_category_books_url


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError
   

def download_txt(url, number, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    params = {'id' : number}
    response = requests.get(url, params=params)
    response.raise_for_status() 
    check_for_redirect(response)
    filepath = os.path.join(folder, f'{sanitize_filename(filename)}.txt')
    with open(filepath, 'wb') as file:
        file.write(response.content)


def download_image(image_url, folder='images/'):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(image_url)
    response.raise_for_status() 
    check_for_redirect(response)
    image_name = urlsplit(image_url).path.split('/')[-1]
    filepath = os.path.join(folder, image_name)
    with open(unquote(filepath), 'wb') as file:
        file.write(response.content)


def parse_book_page(response, template_url):
    soup = BeautifulSoup(response.text, 'lxml')
    book_image_selector = 'div.bookimage img'
    book_image_url = soup.select_one(book_image_selector)['src']
    full_image_url = urljoin(template_url, book_image_url)
    title = soup.select_one('h1').text
    book_title, book_author = title.split(' :: ')
    book_comments_selector = 'div.texts span.black'
    book_comments = soup.select(book_comments_selector)
    comments = [comment.text for comment in book_comments]
    books_genres_select = 'span.d_book a'
    books_genres = soup.select(books_genres_select)
    books_genres = [genre.text for genre in books_genres]
    book_parameters = {
        "title": book_title.strip(),
        "author": book_author.strip(),
        "image_url": full_image_url,
        "genre": books_genres,
        "comments": comments
    }
    return book_parameters


def main():
    parser = argparse.ArgumentParser(
        description= "Проект скачивает книги и соответствующие им картинки,\
                     а также собирает информацию о книге"
    )
    parser.add_argument(
        "--start_page",
        type=int,
        help="Стартовая страница для скачивания",
        default=1
    )
    parser.add_argument(
        "--end_page", 
        type=int,
        help="Конечная страница для скачивания", 
        default=702
        )
    parser.add_argument(
        "--dest_folder",
        help="Путь к каталогу с результатами парсинга",
        default="media"
    )
    parser.add_argument(
        "--skip_imgs",
        action="store_true",
        help="Не скачивать картинки"
    )
    parser.add_argument(
        "--skip_txt",
        action="store_true",
        help="Не скачивать книги"
    )
    parser.add_argument(
        "--json_path",
        help="Путь к JSON файлу с информацией о книгах",
        default="media"
    )
    args = parser.parse_args()
    imgs_dir = f"./{args.dest_folder}/images"
    books_dir = f"./{args.dest_folder}/books"

    os.makedirs(imgs_dir, exist_ok=True)
    os.makedirs(books_dir, exist_ok=True)

    all_books_parameters = []
    
    for number, category_url in enumerate(get_category_books_url(args.start_page, args.end_page)):
        try:
            response = requests.get(category_url)
            response.raise_for_status() 
            check_for_redirect(response)
            book_parameters = parse_book_page(response, category_url)
            all_books_parameters.append(book_parameters)
            if not args.skip_imgs:
                download_image(book_parameters['image_url'], folder=imgs_dir)
            book_title = book_parameters['title']
            filename = f'{number}. {book_title.strip()}'
            url_txt_book = f'https://tululu.org/txt.php'
            if not args.skip_txt:
                download_txt(url_txt_book, number, filename, folder=books_dir)
        except requests.exceptions.HTTPError:
            print('книга не найдена')
        except requests.exceptions.ConnectionError:
            print("Повторное подключение к серверу")
            sleep(20)
    book_parameters_json = json.dumps(all_books_parameters, ensure_ascii=False)
    with open("books.json", "w", encoding='utf8') as my_file:
        my_file.write(book_parameters_json)
   

if __name__=='__main__':
    main()