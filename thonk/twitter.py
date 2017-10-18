from peony import PeonyClient
from os import getenv
from . import utils

if getenv("TWITTER_CONFIG"):
    twitter_opts = utils.load_json(getenv("TWITTER_CONFIG"))
    twitter_bot = PeonyClient(**twitter_opts)

async def tweet(message: str):
    return await twitter_bot.api.statuses.update.post(status=message)
