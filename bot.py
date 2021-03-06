from discord.ext import commands
from os import getenv
from thonk import utils, twitter, twilio

import logging

logging.basicConfig(format="[%(name)s %(levelname)s] %(message)s", level=logging.INFO)

config = utils.read_ini(getenv('CONFIG') or 'configs/config.ini')
botcfg = config['bot']
secret_config = utils.read_ini(botcfg['secrets'])

logging.root.setLevel(config.get('bot', 'log_level', fallback='WARN'))

prefixes = botcfg.get('command_prefixes').split(',')
prefixes = [p.strip() for p in prefixes]

logger = logging.getLogger("thonk")

logger.info(f"Using command prefixes: {', '.join(prefixes)}")

bot = commands.Bot(command_prefix=prefixes, description=botcfg.get('description'))
bot.config = config
bot.secret_config = secret_config

if config.has_option('twitter', 'config'):
    bot.twitter = twitter.Twitter(config.get('twitter', 'config', fallback=None))

if secret_config.has_section('twilio'):
    bot.twilio = twilio.Twilio(secret_config['twilio'])

@bot.command()
async def reload(ctx: commands.Context, *args):
    """Reloads a cog."""

    if len(args) < 1:
        cogs = list(bot.extensions.keys())
        for cog in cogs:
            logger.info(f"Unloading Cog: {cog}")
            bot.unload_extension(cog)
        utils.load_all_cogs(bot)
        await ctx.send(f"Reloaded {len(cogs)} extensions.")
        return

    cog_name = args[0]

    if not cog_name.startswith("cogs."):
        cog_name = "cogs." + cog_name

    logger.info(f"Reloading Cog: {cog_name}")
    bot.unload_extension(cog_name)
    bot.load_extension(cog_name)

    await ctx.send(f"Reloaded: `{cog_name}`.")


utils.load_all_cogs(bot)

logger.info("Connecting...")
bot.run(secret_config['discord']['token'])
