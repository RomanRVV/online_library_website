import json
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
import os


def refresh_website():

    with open("media/books_info.json", "r", encoding='utf-8') as file:
        books_json = file.read()
    all_books = json.loads(books_json)

    os.makedirs('pages', exist_ok=True)
    pages = list(chunked(all_books, 20))

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    for page_number, books in enumerate(pages):
        books_by_columns = chunked(books, 2)
        rendered_page = template.render(books_by_columns=books_by_columns,
                                        page_number=page_number,
                                        number_of_pages=len(pages))
        print(len(pages))
        page_path = f'pages/index{page_number}.html'

        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)


refresh_website

server = Server()
server.watch('template.html', refresh_website)
server.serve(root='.')
