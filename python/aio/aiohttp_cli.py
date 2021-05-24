"""
python -m aiohttp.web aiohttp_cli:init_func
"""
from aiohttp import web


async def hello(request):
    return web.Response(text="Hello, world")


def init_func(argv):
    app = web.Application()
    app.router.add_get("/", hello)
    return app
