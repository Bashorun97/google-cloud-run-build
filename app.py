import random
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    random_value = random.randint(0, 10000)
    return f'<h1>Your magic number is: {int(random_value)} </h2>'


if __name__ == '__main__':
    app.run(port=5000)