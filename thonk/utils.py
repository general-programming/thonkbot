import pkgutil

def get_all_cogs():
    for _, name in pkgutil.iter_modules(["cogs"]):
        yield name
