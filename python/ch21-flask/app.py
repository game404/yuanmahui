# app.py
from werkzeug.middleware.dispatcher import \
    DispatcherMiddleware  # use to combine each Flask app into a larger one that is dispatched based on prefix
from flask_app_1 import app as flask_app_1
from flask_app_2 import app as flask_app_2

application = DispatcherMiddleware(flask_app_1, {
    '/flask_app_2': flask_app_2
})
