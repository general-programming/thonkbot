from discord.ext import commands

class Bucket:
    @commands.command(aliases=['b'])
    async def bucket(self, ctx):
        await ctx.send("Hello, world!")

def setup(bot: commands.Bot):
    bot.add_cog(Bucket())
