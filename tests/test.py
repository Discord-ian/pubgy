import pubgy
import asyncio
import logging

client = pubgy.Pubgy(auth_token="test123123")
loop = client.loop
logging.basicConfig(level=logging.DEBUG)



async def getMatch():
    match = await client.get_match_info()
    print(match.winner)
    print(match.id)

loop.run_until_complete(asyncio.wait([asyncio.ensure_future(getMatch())]))
loop.close()