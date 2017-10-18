from peony import PeonyClient
from os import getenv
from io import BytesIO
from . import utils

if utils.is_deployed():
    twitter_opts = utils.load_json(getenv("TWITTER_CONFIG"))
    twitter_bot = PeonyClient(**twitter_opts)

async def tweet(message: str, **kwargs):
    return await twitter_bot.api.statuses.update.post(status=message, **kwargs)

async def upload(fp: BytesIO):
    return await twitter_bot.upload_media(fp)
