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
        # TODO  并发不有序?
        original_pokemon = await asyncio.gather(*tasks)
        for pokemon in original_pokemon:
            print(pokemon)


asyncio.run(main())

print("--- %s seconds ---" % (time.time() - start_time))
