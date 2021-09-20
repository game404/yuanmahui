import threading
import time

from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def hello():
    do_task(id(request))
    return 'Hello, World!'


def do_task(index):
    t = threading.Thread(target=lambda idx: time.sleep(1), args=(index,))
    t.start()
