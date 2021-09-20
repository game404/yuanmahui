import time

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    time.sleep(1)
    return 'Hello, World!'

