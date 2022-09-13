""" Main application """

import logging
import os
from random import choice
from string import ascii_lowercase
from flask import (Flask, jsonify, make_response, request, send_file, send_from_directory, render_template)
from flask_cors import CORS
from paste.translogger import TransLogger
from waitress import serve
from .model import BookInventory
from .validator import validate_input

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
CORS(app, resources={"*": {"origins": "['https://petstore.swagger.io']"}})
book_inventory = BookInventory()

app_name = os.environ.get('RADIX_APP', f'{"".join(choice(ascii_lowercase) for _i in range(4))}-inventory')


@app.route('/api/books', methods=['GET'])
def api_get_books():
    if len(request.args) == 0:
        return "Missing query parameter 'q'", 400
    elif 'q' not in request.args:
        return "Unknown query parameters", 400
    keyword = request.args['q']
    return jsonify(book_inventory.search(keyword))


@app.route('/api/books/<book_id>', methods=['GET'])
def api_get_book(book_id):
    if int(book_id) < 0:
        raise Exception(f'Negative book id {book_id}')
    book = book_inventory.get_book(book_id)
    if not book:
        return "Book id not found", 404
    return jsonify(book)


@app.route('/api/books', methods=['POST'])
def api_add_book():
    body = request.get_json(silent=True)
    (valid, message) = validate_input(body)
    if not valid:
        return message, 400
    book = book_inventory.add_book(body['title'], body['author'], body['abstract'])
    return jsonify(book), 201


@app.route('/api/books/<book_id>', methods=['PUT'])
def api_update_book(book_id):
    if not book_inventory.has_book(book_id):
        return f'Book with id {book_id} not found', 404
    body = request.get_json()
    (valid, message) = validate_input(body)
    if not valid:
        return message, 400
    book = book_inventory.update_book(book_id, body['title'], body['author'], body['abstract'])
    return jsonify(book), 200


@app.route('/api/books/<book_id>', methods=['DELETE'])
def api_delete_book(book_id):
    if not book_inventory.has_book(book_id):
        return f'Book with id {book_id} not found', 404
    book_inventory.delete_book(book_id)
    return "", 204


@app.route('/')
def send_index():
    return send_file('static/index.html')


@app.route('/openapi.yaml')
def send_openapi():
    host_url = f'https://{request.host}' if "radix" in request.host else request.host_url.rstrip('/')
    response = make_response(render_template('openapi.yaml', host_url=host_url))
    response.headers['content-type'] = 'text/plain; charset=UTF-8'
    return response


@app.route('/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


if __name__ == "__main__":
    logger = logging.getLogger('waitress')
    logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))
    port = int(os.environ.get('PORT', 8080))
    logger.warning('Starting app %s on port %s', app_name, port)
    serve(TransLogger(app, logger=logger, setup_console_handler = False), host='0.0.0.0', port=port)
    