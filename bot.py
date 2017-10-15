from discord.ext import commands
from os import getenv
from thonk import utils

bot = commands.Bot("\u2b6e")

class MainCog:
    async def on_ready(self):
        print(f"Logged in as {bot.user.name}.")

    @commands.command()
    async def reload(self, ctx: commands.Context, cog_name: str):
        if not cog_name.startswith("cogs."):
            cog_name = "cogs." + cog_name

        bot.unload_extension(cog_name)
        bot.load_extension(cog_name)

        await ctx.send(f"Reloaded cog `{cog_name}`.")

    @commands.command()
    async def restart(self, ctx: commands.Context):
        await ctx.send("Going down!")
        await bot.logout()

bot.add_cog(MainCog())

for cog_name in utils.get_all_cogs():
    bot.load_extension(cog_name)

bot.run(token=getenv("TOKEN"))
