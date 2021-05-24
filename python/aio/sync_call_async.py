import asyncio
import logging

logging.getLogger('asyncio').setLevel(logging.INFO)

def test_0():
    async def get_chat_id(name):
        await asyncio.sleep(3)
        return "chat-%s" % name

    def main():
        # SyntaxError: 'await' outside async function
        # result = await get_chat_id("game_404")
        # print(result)
        pass

    main()


def test_1():
    async def get_chat_id(name):
        await asyncio.sleep(3)
        return "chat-%s" % name

    def main():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(get_chat_id("game_404"))
        print(result)

    main()


def test_2():
    async def get_chat_id(name):
        await asyncio.sleep(3)
        return "chat-%s" % name

    def main():
        from asgiref.sync import async_to_sync
        result = async_to_sync(get_chat_id)("game_404")
        print(result)

    main()


def test_3():
    from asgiref.sync import async_to_sync

    @async_to_sync
    async def get_chat_id(name):
        await asyncio.sleep(3)
        return "chat-%s" % name

    def main():
        result = get_chat_id("game_404")
        print(result)

    main()


def test_4():
    from asgiref.sync import async_to_sync

    @async_to_sync
    async def get_chat_id(name):
        await asyncio.sleep(1)
        return "chat-%s" % name

    def main():
        import time
        start = time.perf_counter()
        for x in range(10):
            result = get_chat_id("game_404")
            print(result)
        print(f"Elapsed time: {time.perf_counter() - start}")

    main()


def test_5():
    from asgiref.sync import async_to_sync

    async def get_chat_id(name):
        await asyncio.sleep(1)
        return "chat-%s" % name

    @async_to_sync
    async def batch():
        l = await asyncio.gather(*(get_chat_id(x) for x in range(10)))
        print(l)

    def main():
        import time
        start = time.perf_counter()
        batch()
        print(f"Elapsed time: {time.perf_counter() - start}")

    main()


if __name__ == '__main__':
    test_5()
