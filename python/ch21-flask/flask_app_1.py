# /flask_1/__init__.py
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return '<h1>Hello, World! I am Flask App 1.</h1> \
        Please go visit <a href="/flask_app_2">Flask App 2</a>'
