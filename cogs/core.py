from discord.ext import commands
from raven import Client
from thonk import utils
from thonk.sentry import AioHttpTransport
from traceback import print_exception
import time

class Core:
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        if utils.is_deployed():
            self.raven = Client(transport=AioHttpTransport)

    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}.")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandInvokeError):
            if hasattr(self, "raven"):
                self.raven.captureException(exc_info=utils.exc_info(error.original))
            error = error.original

        if not utils.is_deployed():
            print_exception(*utils.exc_info(error))

        await ctx.send("\N{ANGER SYMBOL} There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        diff = round((t2-t1)*1000)
        await ctx.send(f"Pong! {diff}ms")

    @commands.command()
    async def pong(self, ctx):
        """Pong?"""
        await ctx.send(f"I hear {ctx.author.name} likes cute Asian boys.")

    @commands.command()
    async def cogs(self, ctx):
        """
        Lists all cogs.
        """
        cogs = '\n'.join(map(utils.get_pretty_cog_name, ctx.bot.cogs.values()))
        await ctx.send(f"```\n{cogs}```")

    @commands.command()
    async def extensions(self, ctx):
        """
        Lists all extensions.
        """
        extensions = '\n'.join(ctx.bot.extensions.keys())
        await ctx.send(f"```\n{extensions}```")

    @commands.command()
    async def echo(self, ctx, *, arg):
        """
        Echos a raw message.
        """
        await ctx.send(arg)

    @commands.command(name="eval", hidden=True)
    @utils.require_tag('owner')
    async def _eval(self, ctx, *, arg):
        """
        Evaluates a raw message.
        """
        try:
            result = eval(arg)
        except:
            await ctx.send()
        else:
            await ctx.send(f"```{result}```")

    @commands.command()
    @utils.is_bot_moderator
    async def restart(self, ctx: commands.Context):
        """
        Restart the bot.
        """
        await ctx.send("Going down!")
        await self.bot.logout()

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
