from peony import PeonyClient
from os import getenv
import json

with open(getenv("TWITTER_CONFIG"), mode='r') as file:
    twitter_opts = json.load(file)

twitter_bot = PeonyClient(**twitter_opts)

async def tweet(message: str):
    return await twitter_bot.api.statuses.update.post(status=message)
