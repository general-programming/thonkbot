from discord.ext import commands
import discord
import pkgutil
import inspect
import json
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
    return type(exception), exception, exception.__traceback__


def load_json(filename: str, **kwargs):
    with open(filename, mode='r') as file:
        return json.load(file, **kwargs)

def dump_json(obj, filename: str, **kwargs):
    with open(filename, mode='w') as file:
        return json.dump(obj, filename, **kwargs)



def cog_get_pretty_name(cog):
    if cog is None: return None

    doc = inspect.getdoc(cog)
    return doc if doc is not None else cog.__class__.__name__

permissions = load_json('data/permissions.json')
def require_tag(tag):
    def predicate(ctx):
        for role in ctx.author.roles:
            id = str(role.id)
            if id in permissions['roles']:
                perms = permissions['roles'][id]
                if 'tags' in perms:
                    if tag in perms['tags']:
                        return True
        return False
    return commands.check(predicate)

def is_deployed() -> bool:
    return os.getenv("DEPLOY") == "PRODUCTION"

# use require_tag() instead
def _is_moderator_predicate(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        return False

    role = discord.utils.get(ctx.author.roles, id=369280277840789505)
    return role is not None

is_bot_moderator = commands.check(_is_moderator_predicate)
