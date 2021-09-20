# -*- coding: utf-8 -*-
"""
    shortly
    ~~~~~~~

    A simple URL shortener using Werkzeug and redis.

    :copyright: 2007 Pallets
    :license: BSD-3-Clause
"""
import os

import redis
from jinja2 import Environment
from jinja2 import FileSystemLoader
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.routing import Map
from werkzeug.routing import Rule
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
from werkzeug.wrappers import Request
from werkzeug.wrappers import Response


def base36_encode(number):
    assert number >= 0, "positive integer required"
    if number == 0:
        return "0"
    base36 = []
    while number != 0:
        number, i = divmod(number, 36)
        base36.append("0123456789abcdefghijklmnopqrstuvwxyz"[i])
    return "".join(reversed(base36))


def is_valid_url(url):
    parts = url_parse(url)
    return parts.scheme in ("http", "https")


def get_hostname(url):
    return url_parse(url).netloc


class Shortly(object):
    def __init__(self, config):
        self.redis = redis.Redis(config["redis_host"], config["redis_port"])
        template_path = os.path.join(os.path.dirname(__file__), "templates")
        self.jinja_env = Environment(
            loader=FileSystemLoader(template_path), autoescape=True
        )
        self.jinja_env.filters["hostname"] = get_hostname

        self.url_map = Map(
            [
                Rule("/", endpoint="new_url"),
                Rule("/echo", endpoint="echo"),
                Rule("/<short_id>", endpoint="follow_short_link"),
                Rule("/<short_id>+", endpoint="short_link_details"),
            ]
        )

    def on_echo(self, request):
        raise

    def on_new_url(self, request):
        error = None
        url = ""
        if request.method == "POST":
            url = request.form["url"]
            if not is_valid_url(url):
                error = "Please enter a valid URL"
            else:
                short_id = self.insert_url(url)
                return redirect("/%s+" % short_id)
        return self.render_template("new_url.html", error=error, url=url)

    def on_follow_short_link(self, request, short_id):
        link_target = self.redis.get("url-target:" + short_id)
        if link_target is None:
            raise NotFound()
        self.redis.incr("click-count:" + short_id)
        return redirect(link_target)

    def on_short_link_details(self, request, short_id):
        link_target = self.redis.get("url-target:" + short_id)
        print("b")
        if link_target is None:
            raise NotFound()
        click_count = int(self.redis.get("click-count:" + short_id) or 0)
        return self.render_template(
            "short_link_details.html",
            link_target=link_target,
            short_id=short_id,
            click_count=click_count,
        )

    def error_404(self):
        response = self.render_template("404.html")
        response.status_code = 404
        return response

    def insert_url(self, url):
        short_id = self.redis.get("reverse-url:" + url)
        if short_id is not None:
            return short_id
        url_num = self.redis.incr("last-url-id")
        short_id = base36_encode(url_num)
        self.redis.set("url-target:" + short_id, url)
        self.redis.set("reverse-url:" + url, short_id)
        return short_id

    def render_template(self, template_name, **context):
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype="text/html")

    def dispatch_request(self, request):
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            endpoint, values = adapter.match()
            return getattr(self, "on_" + endpoint)(request, **values)
        except NotFound:
            return self.error_404()
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host="localhost", redis_port=6379, with_static=True):
    app = Shortly({"redis_host": redis_host, "redis_port": redis_port})
    if with_static:
        app.wsgi_app = SharedDataMiddleware(
            app.wsgi_app, {"/static": os.path.join(os.path.dirname(__file__), "static")}
        )
    return app


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    # os.environ["WERKZEUG_DEBUG_PIN"] = "off"
    app = create_app()
    run_simple("127.0.0.1", 5000, app, use_debugger=True, use_reloader=True, use_evalex=True)
