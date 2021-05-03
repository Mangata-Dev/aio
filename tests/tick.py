import aiohttp
import asyncio
from rich import print

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:9000/tick/') as response:

            # print("Status:", response.status)
            # print("Content-type:", response.headers['content-type'])


            # print("Body:", html[:15], "...")
            print(await response.json())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())