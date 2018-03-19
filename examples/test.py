import pubgy
import logging
import asyncio

client = pubgy.Pubgy(auth_token="your token here")
loop = client.loop
logging.basicConfig(level=logging.DEBUG)


async def getMatch():
    match = await client.match(page_length=1)
    print("The match id was {}".format(match.id))
    print("The URL for telemetry is {}".format(match.telemetry.url))


loop.run_until_complete(asyncio.wait([asyncio.ensure_future(getMatch())]))
client.close()
# client.close is now required to avoid asyncio errors
