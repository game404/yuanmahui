import asyncio

TIMEOUT = 1  # Second


class FlowControlServer(asyncio.Protocol):
    def __init__(self):
        self._can_write = asyncio.Event()
        self._can_write.set()

    def pause_writing(self) -> None:
        # Will be called whenever the transport crosses the
        # high-water mark.
        self._can_write.clear()

    def resume_writing(self) -> None:
        # Will be called whenever the transport drops back below the
        # low-water mark.
        self._can_write.set()

    async def drain(self) -> None:
        await self._can_write.wait()


class TimeoutServer(asyncio.Protocol):
    def __init__(self):
        loop = asyncio.get_running_loop()
        self.timeout_handle = loop.call_later(
            TIMEOUT, self._timeout,
        )

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        self.timeout_handle.cancel()

    def _timeout(self):
        self.transport.close()


async def main(host, port):
    loop = asyncio.get_running_loop()
    server = await loop.create_server(TimeoutServer, host, port)
    await server.serve_forever()


asyncio.run(main('127.0.0.1', 5000))
