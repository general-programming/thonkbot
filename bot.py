from discord.ext import commands
from os import getenv
from thonk import utils, formatter

print()

config = utils.read_ini(getenv('CONFIG') or 'configs/config.ini')
botcfg = config['bot']

prefixes = botcfg.get('command_prefixes').split(',')
prefixes = [p.strip() for p in prefixes]

print(f"Using command prefixes: {', '.join(prefixes)}")

bot = commands.Bot(command_prefix=prefixes, description=botcfg.get('description'), formatter=formatter.CustomHelpFormatter())
bot.config = config

@bot.command()
async def reload(ctx: commands.Context, *args):
    """Reloads a cog."""

    if len(args) < 1:
        cogs = list(bot.extensions.keys())
        for cog in cogs:
            print(f"Unloading Cog: {cog}")
            bot.unload_extension(cog)
        utils.load_all_cogs(bot)
        await ctx.send(f"Reloaded {len(cogs)} extensions.")
        return

    cog_name = args[0]

    if not cog_name.startswith("cogs."):
        cog_name = "cogs." + cog_name

    print(f"Reloading Cog: {cog_name}")
    bot.unload_extension(cog_name)
    bot.load_extension(cog_name)

    await ctx.send(f"Reloaded: `{cog_name}`.")


utils.load_all_cogs(bot)

print("Connecting...")
bot.run(getenv('TOKEN'))
