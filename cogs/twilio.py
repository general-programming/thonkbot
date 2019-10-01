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
    def __init__(self, twilio: Twilio):
        self.twilio = twilio

    @commands.command()
    @utils.require_tag("employee")
    async def sms(self, ctx: Context, phone: PhoneConverter, *, arg: str):
        try:
            await self.twilio.send_sms(phone, arg)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        except Exception:
            await ctx.message.add_reaction("\N{CROSS MARK}")
            raise

    @commands.command()
    @utils.require_tag("employee")
    async def mms(self, ctx: Context, phone: PhoneConverter, *, arg: str = None):
        if len(ctx.message.attachments) is 0:
            raise commands.CommandError("Attachment is required for MMS")

        attachments = [i.url for i in ctx.message.attachments if i.url]
        try:
            await self.twilio.send_mms(phone, attachments, arg)
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        except Exception:
            await ctx.message.add_reaction("\N{CROSS MARK}")
            raise



def setup(bot):
    bot.add_cog(TwilioCog(bot.twilio))
