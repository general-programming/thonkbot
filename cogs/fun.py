from discord.ext import commands

class FunCog:
    """Fun"""

    @commands.command()
    async def pong(self, ctx):
        """Pong?"""
        await ctx.send(f"I hear {ctx.author.name} likes cute Asian boys.")


def setup(bot):
    bot.add_cog(FunCog())
