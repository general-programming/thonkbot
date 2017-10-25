from discord.ext import commands

class RockPaperScissors:
    """Rock, Paper, Scissors!"""
    @commands.command()
    async def rock(self, ctx):
        """Rock beats scissors!"""
        await ctx.send('paper')

    @commands.command()
    async def paper(self, ctx):
        """Paper beats rock!"""
        await ctx.send('scissors')

    @commands.command()
    async def scissors(self, ctx):
        """Scissors beats paper!"""
        await ctx.send('rock')

def setup(bot):
    bot.add_cog(RockPaperScissors())
