from flask import Flask, request

from myapp import add

app = Flask(__name__)


@app.route('/')
def hello():
    ret = add.delay(id(request), id(request))
    print("hello", id(request), ret)
    print(ret.get())
    return 'Hello, World!'
