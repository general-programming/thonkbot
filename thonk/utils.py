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
