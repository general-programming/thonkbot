import pkgutil
import json
import os

from discord.ext import commands

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

with open('permissions.json') as data_file:
    permissions = json.load(data_file)

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
