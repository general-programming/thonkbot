from discord.ext import commands
from configparser import ConfigParser
from io import BytesIO
import discord
import pkgutil
import inspect
import json
import sys
import os

def get_all_cogs():
    for _, name, _ in pkgutil.iter_modules(["cogs"]):
        yield f"cogs.{name}"

def load_all_cogs(bot):
    for cog_name in get_all_cogs():
        print(f"Loading Cog: {cog_name}")
        bot.load_extension(cog_name)

def safe_text(text: str):
    """
    Escapes markdown formatting in text to avoid it closing formatting blocks early.
    """
    return text.replace("*", "\u2217")\
               .replace("`", "\u02cb")

def exc_info(exception: Exception):
    return type(exception), exception, exception.__traceback__


def load_json(filename: str, **kwargs):
    with open(filename, 'r', encoding='utf8') as file:
        return json.loads(file.read(), **kwargs)

def dump_json(obj, filename: str, **kwargs):
    with open(filename, mode='w', encoding='utf8') as file:
        return json.dump(obj, file, **kwargs)

def read_ini(filename, base={}):
    cfg = ConfigParser()
    print(f"Reading Config: {filename}")
    with open(filename, 'r', encoding='utf8') as file:
        cfg.read_string('[_meta]\n' + file.read())
    base_path = cfg.get('_meta', 'base', fallback=None)
    if base_path:
        cfg = read_ini(os.path.join(os.path.dirname(filename), base_path), cfg)
    cfg.read_dict(base)
    return cfg


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

async def to_fp(attachment: discord.Attachment):
    bio = BytesIO()
    await attachment.save(bio)
    bio.seek(0)

    return bio

def is_deployed(bot):
    return bot.config.get('bot', 'environment', fallback='development') == 'production'

# use require_tag() instead
def _is_moderator_predicate(ctx: commands.Context):
    if not isinstance(ctx.channel, discord.abc.GuildChannel):
        return False

    role = discord.utils.get(ctx.author.roles, id=369280277840789505)
    return role is not None

is_bot_moderator = commands.check(_is_moderator_predicate)
