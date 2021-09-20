# /flask_2/__init__.py
from flask import Flask

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return '<h1>Hello, World! I am Flask App 2.</h1> \
        Please go visit <a href="/">Flask App 1</a>'
