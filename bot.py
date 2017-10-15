from discord.ext import commands
from os import getenv
from thonk import utils

#bot = commands.Bot(command_prefix="$", description="ThonkBot")
bot = commands.Bot(command_prefix="\u2b6e", description="ThonkBot")

def load_all_cogs():
    for cog_name in utils.get_all_cogs():
        bot.load_extension(cog_name)

@bot.command()
async def reload(ctx: commands.Context, *args):
    """Reloads a cog."""

    if len(args) < 1:
        cogs = bot.extensions.keys()
        for cog in cogs:
            bot.unload_extension(cog)
        load_all_cogs()
        return

    cog_name = args[0]

    if not cog_name.startswith("cogs."):
        cog_name = "cogs." + cog_name

    bot.unload_extension(cog_name)
    bot.load_extension(cog_name)

    await ctx.send(f"Reloaded: `{cog_name}`.")


load_all_cogs()

print("Connecting...")
bot.run(getenv('TOKEN'))
