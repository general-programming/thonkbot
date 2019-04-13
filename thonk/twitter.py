from peony import PeonyClient
from io import BytesIO
from . import utils


class Twitter:
    def __init__(self, config_path: str):
        self._config = utils.load_json(config_path)
        self.twitter = PeonyClient(**self._config)

    async def tweet(self, message: str, **kwargs):
        return await self.twitter.api.statuses.update.post(status=message, **kwargs)

    async def upload(self, fp: BytesIO):
        return await self.twitter.upload_media(fp)

    def fetch_tweet(self, snowflake):
        return self.twitter.api.statuses.show.get(id=snowflake, tweet_mode='extended')
