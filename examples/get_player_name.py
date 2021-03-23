import pubgy
import logging
import asyncio

client = pubgy.Pubgy("PUT KEY HERE")
loop = client.loop
logging.basicConfig(level=logging.DEBUG)

async def mainExample():
    name = input("What is the name of the player you want to search for \n>")
    shard = input("What shard does that player exist on? (steam/psn/xbox/stadia) \n>")
    ply = await client.get_player(name, shard=shard)
    print("That player's name is {0.name} and their ID is {0.id}".format(ply))

loop.run_until_complete(mainExample())
