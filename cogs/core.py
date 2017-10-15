from thonk import utils
from discord.ext import commands

class Core:
    def __init__(self, bot):
        self.bot = bot

    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}.")

    async def on_command_error(self, ctx, error):
        name = type(error).__name__
        if type(error) is commands.CommandInvokeError:
            error = error.original
            name = type(error).__name__
            await ctx.send(f"\N{ANGER SYMBOL} There was an internal error! ({name})")
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        else:
            await ctx.send("\N{ANGER SYMBOL} There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")

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

    @commands.command()
    async def eval(self, ctx, *, arg):
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
