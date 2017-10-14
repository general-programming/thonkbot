import pkgutil

def get_all_cogs():
    for _, name, _ in pkgutil.iter_modules(["cogs"]):
        yield f"cogs.{name}"
