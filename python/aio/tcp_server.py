"""
https://medium.com/@pgjones/an-asyncio-socket-tutorial-5e6f3308b8b0
"""

import asyncio


async def echo_server(reader, writer):
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            break
        writer.write(data)
        await writer.drain()  # Flow control, see later
    writer.close()


async def main(host, port):
    server = await asyncio.start_server(echo_server, host, port)
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
