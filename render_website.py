import argparse
import json
import os

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


def refresh_website(path):

    with open(path, "r", encoding='utf-8') as file:
        all_books = json.load(file)
    os.makedirs('pages', exist_ok=True)

    books_per_page = 20
    pages = list(chunked(all_books, books_per_page))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    for page_number, books in enumerate(pages):
        number_of_chunks = 2
        books_by_columns = chunked(books, number_of_chunks)
        rendered_page = template.render(books_by_columns=books_by_columns,
                                        page_number=page_number,
                                        number_of_pages=len(pages))
        page_path = f'pages/index{page_number}.html'

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    parser = argparse.ArgumentParser(description='Скрипт создает статический сайт')
    parser.add_argument('--path',
                        help='укажите путь к json файлу',
                        default='media/books_info.json')
    args = parser.parse_args()

    refresh_website(args.path)

    server = Server()
    server.watch('template.html', refresh_website)
    server.serve(root='.')


if __name__ == '__main__':
    main()
