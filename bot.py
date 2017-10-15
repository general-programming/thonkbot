from discord.ext import commands
from os import getenv
from thonk import utils

bot = commands.Bot("\u2b6e")

class MainCog:
    async def on_ready(self):
        print(f"Logged in as {bot.user.name}.")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await ctx.send("\N{ANGER SYMBOL} There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")

    @commands.command()
    async def reload(self, ctx: commands.Context, cog_name: str):
        """
        Reload a module.
        """
        if not cog_name.startswith("cogs."):
            cog_name = "cogs." + cog_name

        bot.unload_extension(cog_name)
        bot.load_extension(cog_name)

        await ctx.send(f"Reloaded cog `{cog_name}`.")

    @commands.command()
    async def restart(self, ctx: commands.Context):
        """
        Restart the bot.
        """
        await ctx.send("Going down!")
        await bot.logout()

bot.add_cog(MainCog())

for cog_name in utils.get_all_cogs():
    bot.load_extension(cog_name)

bot.run(getenv("TOKEN"))
