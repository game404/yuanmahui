import threading
import time
import random

from flask import Flask, g, request

app = Flask(__name__)


@app.route('/')
def hello():
    print("->", threading.active_count(), threading.get_ident(), request)
    r = random.randint(1, 5)
    time.sleep(r)
    print("<-", threading.active_count(), threading.get_ident(), r, request)
    return 'Hello, World!'
