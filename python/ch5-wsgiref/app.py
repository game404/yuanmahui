from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

from bottle import Bottle

from pycallgraph import PyCallGraph
from pycallgraph import Config
from pycallgraph import GlobbingFilter
from pycallgraph.output import GraphvizOutput


def make_server(
    host, port, app, server_class=WSGIServer, handler_class=WSGIRequestHandler
):
    """Create a new WSGI server listening on `host` and `port` for `app`"""
    server = server_class((host, port), handler_class)
    server.set_app(app)
    return server


config = Config(max_depth=200)
config.trace_filter = GlobbingFilter(include=[
    'socketserver.*',
    'http.server.*'
    'wsgiref.*',
    'selectors.*',
    'bottle.*'
])
graphviz = GraphvizOutput(output_file='grpah.png')


if __name__ == '__main__':
    with PyCallGraph(output=graphviz, config=config):
        app = Bottle()

        @app.route('/hello')
        def hello():
            return "Hello World!"
        with make_server('', 8000, app) as httpd:
            sa = httpd.socket.getsockname()
            print("Serving HTTP on", sa[0], "port", sa[1], "...")
            # import webbrowser
            # webbrowser.open('http://localhost:8000/hello?abc')
            httpd.handle_request()  # serve one request, then exit
