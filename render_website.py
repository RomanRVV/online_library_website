import json
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked

def refresh_website():

    with open("books_info.json", "r", encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')
    books_by_columns = chunked(books, 2)
    rendered_page = template.render(books_by_columns=books_by_columns)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


refresh_website

server = Server()
server.watch('template.html', refresh_website)
server.serve(root='.')
