"""
https://docs.aiohttp.org/en/stable/web_quickstart.html
"""
import json
from aiohttp import web


async def handle(request):
    print(request)
    return web.Response(text=json.dumps({"a": str(10).zfill(10), "b": "a"}))


app = web.Application()
app.add_routes([web.get('/test', handle)])

web.run_app(app)
