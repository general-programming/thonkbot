import pkgutil

def get_all_cogs():
    for _, name, _ in pkgutil.iter_modules(["cogs"]):
        yield f"cogs.{name}"

def safe_text(text: str):
    """
    Escapes markdown formatting in text to avoid it closing formatting blocks early.
    """
    return text.replace("*", "\u2217")\
               .replace("`", "\u02cb")
