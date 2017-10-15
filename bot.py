from discord.ext import commands
from os import getenv
from thonk import utils, formatter

prefixes = [
    "\N{Clockwise Triangle-Headed Open Circle Arrow}",
    "\N{Clockwise Open Circle Arrow}",
    "\N{Clockwise Gapped Circle Arrow}"
]
if getenv('COMMAND_PREFIX'):
    prefixes = getenv('COMMAND_PREFIX')
    print(f"Using custom COMMAND_PREFIX: {prefixes}")

bot = commands.Bot(command_prefix=prefixes, description="ThonkBot", formatter=formatter.CustomHelpFormatter())

def load_all_cogs():
    for cog_name in utils.get_all_cogs():
        print(f"Loading Cog: {cog_name}")
        bot.load_extension(cog_name)

@bot.command()
async def reload(ctx: commands.Context, *args):
    """Reloads a cog."""

    if len(args) < 1:
        cogs = list(bot.extensions.keys())
        for cog in cogs:
            print(f"Unloading Cog: {cog}")
            bot.unload_extension(cog)
        load_all_cogs()
        await ctx.send("Done.")
        return

    cog_name = args[0]

    if not cog_name.startswith("cogs."):
        cog_name = "cogs." + cog_name

    print(f"Reloading Cog: {cog_name}")
    bot.unload_extension(cog_name)
    bot.load_extension(cog_name)

    await ctx.send(f"Reloaded: `{cog_name}`.")


load_all_cogs()

print("Connecting...")
bot.run(getenv('TOKEN'))
