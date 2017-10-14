from discord.ext import commands

class GitManagementCog:
    def __init__(self):
        pass

    def __global_check(self):
        return True

def setup(bot: commands.Bot):
    bot.add_cog(GitManagementCog())
