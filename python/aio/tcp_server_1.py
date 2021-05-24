import asyncio
import functools
import os
import signal


def ask_exit(signame, loop):
    print("got signal %s: exit" % signame)
    loop.stop()


async def echo_server(reader, writer):
    while True:
        data = await reader.read(100)  # Max number of bytes to read
        if not data:
            break
        writer.write(data)
        await writer.drain()  # Flow control, see later
    writer.close()


async def main():
    # loop = asyncio.get_event_loop()
    loop = asyncio.get_running_loop()

    for signame in {'SIGINT', 'SIGTERM'}:
        loop.add_signal_handler(
            getattr(signal, signame),
            functools.partial(ask_exit, signame, loop))
    await asyncio.start_server(echo_server, '127.0.0.1', 5000)
    while True:
        await asyncio.sleep(3600)


print("Event loop running for 1 hour, press Ctrl+C to interrupt.")
print(f"pid {os.getpid()}: send SIGINT or SIGTERM to exit.")

asyncio.run(main())
