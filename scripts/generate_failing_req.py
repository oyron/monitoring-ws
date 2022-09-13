""" Generate traffic to API """
from time import sleep
import requests

SERVER_URL = 'https://<prefix>-inventory.app.playground.radix.equinor.com'
SLEEP_LENGTH = 1500

def print_request(method, url, status_code, request_id):
    print(f'{request_id}: {method} {url}: {status_code}')

def get_book(book_id, counter):
    url = f'{SERVER_URL}/api/books/{book_id}'
    response = requests.get(url)
    print_request('GET', url, response.status_code, counter)


def run():
    counter = 0
    while True:
        get_book(-1, counter)
        sleep(SLEEP_LENGTH/1000)
        counter += 1

if __name__ == "__main__":
    run()
