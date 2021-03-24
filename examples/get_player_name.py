import pubgy
import logging

client = pubgy.Pubgy("PUT KEY HERE")
loop = client.loop
logging.basicConfig(level=logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR


async def get_player():
    name = input("What is the name of the player you want to search for \n>")
    shard = input("What shard does that player exist on? (steam/psn/xbox/stadia) \n>")
    ply = await client.get_player(name, shard=shard)
    print("That player's name is {0.name} and their ID is {0.pId}".format(ply))
    # you can either use player.pId or just a reference to player to get their player ID

loop.run_until_complete(get_player())
