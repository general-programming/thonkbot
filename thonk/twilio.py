from twilio.rest import Client
from . import utils


class Twilio:
    def __init__(self, secrets):
        self.from_ = secrets['from_']
        self.client = Client(secrets['sid'], secrets['token'])

    async def send_sms(self, to, message, from_=None):
        self.client.messages.create(
            body=message,
            from_=from_ if from_ is not None else self.from_,
            to=to,
        )

    async def send_mms(self, to, media, message=None, from_=None):
        self.client.messages.create(
            body=message,
            from_=from_ if from_ is not None else self.from_,
            to=to,
            media_url=media
        )
