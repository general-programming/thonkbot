from discord.ext import commands
from thonk import utils

class FunCog(commands.Cog):
    """Fun"""

    @commands.command()
    async def pong(self, ctx):
        """Pong?"""
        await ctx.send(f"I hear {utils.safe_text(ctx.author.name)} likes cute Asian boys.")


def setup(bot):
    bot.add_cog(FunCog())
