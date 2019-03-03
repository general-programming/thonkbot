from discord.ext import commands
from raven import Client
from thonk import utils
from thonk.sentry import AioHttpTransport
import traceback
import asyncio
import time

class Core:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_result = None

        if utils.is_deployed(bot):
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

        if not utils.is_deployed(ctx.bot):
            traceback.print_exception(*utils.exc_info(error))

        await ctx.send("💢 There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()

        diff = round((t2-t1)*1000)
        await ctx.send(f"Pong! {diff}ms")

    @commands.command()
    async def cogs(self, ctx):
        """
        Lists all cogs.
        """
        cogs = '\n'.join(map(utils.cog_get_pretty_name, ctx.bot.cogs.values()))
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

    def remove_code_tags(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

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
