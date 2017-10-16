from discord.ext import commands
import discord
import pkgutil
import os

def get_all_cogs():
    for _, name, _ in pkgutil.iter_modules(["cogs"]):
        yield f"cogs.{name}"

def safe_text(text: str):
    """
    Escapes markdown formatting in text to avoid it closing formatting blocks early.
    """
    return text.replace("*", "\u2217")\
               .replace("`", "\u02cb")

def exc_info(exception: Exception):
    return (type(exception), exception, exception.__traceback__)

def is_deployed() -> bool:
    return os.getenv("DEPLOY") == "PRODUCTION"

def _is_moderator_predicate(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        return False

    role = discord.utils.get(ctx.author.roles, id=369280277840789505)
    return role is not None

is_bot_moderator = commands.check(_is_moderator_predicate)
