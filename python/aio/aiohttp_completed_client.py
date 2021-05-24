import aiohttp
import asyncio
import time

start_time = time.time()


async def get_pokemon(session, url):
    async with session.get(url) as resp:
        await resp.text()
        return url


async def main():

    async with aiohttp.ClientSession() as session:

        tasks = []
        for number in range(1, 151):
            url = f'http://www.baidu.com?q={number}'
            tasks.append(asyncio.ensure_future(get_pokemon(session, url)))

        for res in asyncio.as_completed(tasks):
            compl = await res
            print(compl)

# asyncio.run(main())

from asgiref.sync import async_to_sync

async def test():
    print("test")
    await main()

async_to_sync(test)()
print("--- %s seconds ---" % (time.time() - start_time))