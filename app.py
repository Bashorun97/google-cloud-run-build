import os
import random
import hashlib
from functools import wraps

from flask import Flask, request, abort


app = Flask(__name__)


def require_apikey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        API_KEY_HEADER_NAME = 'x-api-key'

        if not request.headers.get(API_KEY_HEADER_NAME):
            abort(400, f'{API_KEY_HEADER_NAME} was not found.')

        expected_hashed_api_key = os.environ.get('HASHED_API_KEY')
        received_api_key = request.headers.get(API_KEY_HEADER_NAME)

        received_hashed_api_key = hash_value(received_api_key)

        if expected_hashed_api_key == received_hashed_api_key:
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function


def hash_value(value):
    hash_object = hashlib.sha512(bytearray(value, encoding='utf8'))
    hashed = hash_object.hexdigest()

    return hashed


@app.route('/')
@require_apikey
def index():
    random_value = random.randint(0, 10000)
    return f'<h1>Your magic number is: {int(random_value)}</h1>'


@app.route('/health')
def health():
    return f'<h1>This container is alive</h1>'


if __name__ == '__main__':
    app.run(port=5000)