""" Generate a number of post requests to API """
import sys
from time import sleep
import requests
from essential_generators import DocumentGenerator

gen = DocumentGenerator()

SERVER_URL = 'https://<prefix>-inventory.app.playground.radix.equinor.com'


def print_request(method, url, status_code):
    print(f'{method} {url}: {status_code}')

def post_book(book):
    url = f'{SERVER_URL}/api/books'
    response = requests.post(url, json=book)
    print_request('POST', url, response.status_code)

def generate_book():
    author = f'{gen.word().capitalize()} {gen.word().capitalize()}'
    title = f'{gen.word().capitalize()}'
    abstract = ""
    for _i in range(100000):
        abstract += "Lorem Ipsum "
    return {'author': author, 'title': title, 'abstract': abstract}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Missing parameter <number of iterations>")
    else:
        num_requests = int(sys.argv[1])
        print(f'Generating {num_requests} POST requests')
        for counter in range(1, num_requests + 1):
            print(f'{counter}:')
            post_book(generate_book())
            sleep(0.1)
