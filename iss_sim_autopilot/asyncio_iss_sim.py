import asyncio
import random

async def myCoroutine1s(id):
    process_time = 1
    await asyncio.sleep(process_time)
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, process_time))
async def myCoroutine2s(id):
    process_time = 2
    await asyncio.sleep(process_time)
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, process_time))
async def myCoroutine3s(id):
    process_time = 3
    await asyncio.sleep(process_time)
    print("Coroutine: {}, has successfully completed after {} seconds".format(id, process_time))

async def main():
    tasks = []
    tasks.append(asyncio.ensure_future(myCoroutine1s(1)))
    tasks.append(asyncio.ensure_future(myCoroutine2s(2)))
    tasks.append(asyncio.ensure_future(myCoroutine2s(2)))
    tasks.append(asyncio.ensure_future(myCoroutine3s(3)))

    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close