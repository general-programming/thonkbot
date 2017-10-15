import time
import traceback
import sys
from thonk import utils
from discord.ext import commands

class Core:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}.")

    async def on_command_error(self, ctx, error):
        if type(error) is commands.CommandNotFound:
            return

        if type(error) is commands.CommandInvokeError:
            error = error.original

        await ctx.send("\N{ANGER SYMBOL} There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


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
        cogs = '\n'.join(ctx.bot.extensions.keys())
        await ctx.send(f"```{cogs}```")

    @commands.command()
    async def echo(self, ctx, *, arg):
        """
        Echos a raw message.
        """
        await ctx.send(arg)

    @commands.command(name="eval")
    async def _eval(self, ctx, *, arg):
        """
        Evaluates a raw message.
        """
        result = eval(arg)
        await ctx.send(f"```{result}```")

    @commands.command()
    async def restart(self, ctx: commands.Context):
        """
        Restart the bot.
        """
        await ctx.send("Going down!")
        await self.bot.logout()

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
