from discord.ext import commands
import pubgy

pubg = pubgy.Pubgy(auth_token="YOUR API KEY HERE")
bot = commands.Bot(command_prefix="+")
# set plus as the command prefix.


@bot.event
async def on_ready():
    print("Bot is online.")


@commands.command()
async def match(match_id=None):
    match = await pubg.matches(match_id=match_id)
    await bot.say(
        "Match occured on {} shard. The first player was {}.".format(
            match.shard, match.players[0].name
        )
    )


bot.run("YOUR BOT TOKEN HERE")
