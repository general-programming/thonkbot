import re
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, Converter
from thonk import utils
from thonk.twilio import Twilio


class PhoneConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        stripped = re.sub('[^0-9+]+', '', argument)
        if not re.match('^\+?[1-9]\d{1,14}$', stripped):
            raise commands.UserInputError("A valid E.164 phone no. is required.")

        return stripped


class TwilioCog(Cog):
    """Twilio handler"""

    def __init__(self, twilio: Twilio):
        self.twilio = twilio

    @commands.command(aliases=["sms", "mms", "sendtext"])
    @utils.require_tag("employee")
    async def msg(self, ctx: Context, phone: PhoneConverter, *, arg: str = None):
        """Send a SMS/MMS message"""
        attachments = [i.url for i in ctx.message.attachments if i.url]
        if len(attachments) is 0 and arg is None:
            raise commands.CommandError("Body or attachment required to send message")

        try:
            if len(attachments):
                await self.twilio.send_mms(phone, attachments, arg)
            else:
                await self.twilio.send_sms(phone, arg)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        except Exception:
            await ctx.message.add_reaction("\N{CROSS MARK}")
            raise


def setup(bot):
    if hasattr(bot, 'twilio'):
        bot.add_cog(TwilioCog(bot.twilio))
