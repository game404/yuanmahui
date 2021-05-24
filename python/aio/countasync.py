#!/usr/bin/env python3
# countasync.py

import asyncio


async def count():
    print("One", id(asyncio.current_task()))
    await asyncio.sleep(1)
    print("Two", id(asyncio.current_task()))


async def main():
    await asyncio.gather(count(), count(), count())
    print("main")


if __name__ == "__main__":
    import time

    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

#  get_running_loop() && get_event_loop
