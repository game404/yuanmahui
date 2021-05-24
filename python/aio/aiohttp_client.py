import aiohttp
import asyncio
import time

start_time = time.time()


async def main():

    async with aiohttp.ClientSession() as session:

        for number in range(1, 151):
            pokemon_url = f'http://www.baidu.com?q={number}'
            async with session.get(pokemon_url) as resp:
                await resp.text()
                print(number)

asyncio.run(main())
print("--- %s seconds ---" % (time.time() - start_time))