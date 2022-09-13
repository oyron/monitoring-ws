""" Generate traffic to API """
from json import JSONDecodeError
from random import randint, seed, choice
from time import sleep, time
import requests

SERVER_URL = 'https://<prefix>-inventory.app.playground.radix.equinor.com'
SLEEP_LENGTH = 2000

def print_request(method, url, status_code):
    print(f'{method} {url}: {status_code}')

def get_book(book_id):
    url = f'{SERVER_URL}/api/books/{book_id}'
    response = requests.get(url)
    print_request('GET', url, response.status_code)

def search_books():
    url = f'{SERVER_URL}/api/books?q=Robinson'
    response = requests.get(url)
    print_request('GET', url, response.status_code)

def post_book(book):
    url = f'{SERVER_URL}/api/books'
    response = requests.post(url, json=book)
    print_request('POST', url, response.status_code)
    book_id = None
    try:
        book_id = int(response.json()['id'])
    except JSONDecodeError:
        return -1
    return book_id

def put_book(book, book_id):
    url = f'{SERVER_URL}/api/books/{book_id}'
    response = requests.put(url, json=book, headers={'content-type':'application/json'})
    print_request('PUT', url, response.status_code)

def delete_book(book_id):
    url = f'{SERVER_URL}/api/books/{book_id}'
    response = requests.delete(url)
    print_request('DELETE', url, response.status_code)

def generate_book():
    first_names = ["Ada", "Thor", "Grete", "Martin", "Queen"]
    last_names = ["Hegerberg", "Hushovd", "Waitz", "Fowler", "Elisabeth"]
    title_first_part = ["The", "A", "Never", "Always", "Sometimes"]
    title_last_part = ["Kill", "Save", "Code", "Bias", "Refactoring"]
    author = f'{first_names[randint(0, 4)]} {last_names[randint(0, 4)]}'
    title = f'{title_first_part[randint(0, 4)]} {title_last_part[randint(0, 4)]}'
    description = choice(['dystopian book', 'futuristic masterpiece', 'autobiography', 'science fiction drama'])
    abstract = f'A {description} by {author} about {title.lower()}'
    return {'author': author, 'title': title, 'abstract': abstract}


def do_sleep():
    sleep(randint(0, SLEEP_LENGTH) / 1000)

def run():
    max_id = 0
    counter = 0
    while True:
        seed(time())
        new_id = post_book(generate_book())
        max_id = max(max_id, new_id)
        do_sleep()

        search_books()
        do_sleep()
        
        get_book(randint(0, max_id + int(max_id * 0.5))) # intentionally ranged too high, to sometimes generate 404
        do_sleep()
        
        delete_book(randint(3, max_id))
        do_sleep()
        
        post_book(generate_book())
        do_sleep()
        
        new_id = post_book(generate_book())
        max_id = max(max_id, new_id)
        do_sleep()
        
        put_book(generate_book(), randint(3, max_id + int(max_id * 0.5))) # same as above
        do_sleep()

        if counter % 2 == 0:
            get_book(-1)
        do_sleep()
        counter += 1

if __name__ == "__main__":
    run()
