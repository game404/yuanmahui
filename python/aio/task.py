import asyncio


async def f():
    print("One", id(asyncio.current_task()))
    await asyncio.sleep(1)


def main():
    # a = f() # RuntimeWarning: coroutine 'f' was never awaited
    # loop = asyncio.get_running_loop() # RuntimeError: no running event loop
    loop = asyncio.get_event_loop()
    # loop.call_soon(f)  # RuntimeWarning: coroutine 'f' was never awaited
    loop.run_forever()


if __name__ == '__main__':
    main()
