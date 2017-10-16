from discord.ext import commands
from os import getenv
from thonk import utils
import aiohttp
import json

class GitManagementCog:
    name = "Git Management"

    def __init__(self):
        pass

    async def __local_check(self, ctx: commands.Context):
        return True

    @commands.group(invoke_without_command=True)
    async def git(self, ctx):
        """
        Git management.
        """
        temp_ctx = ctx
        temp_ctx.invoked_with = 'help git'
        pages = await ctx.bot.formatter.format_help_for(ctx, self.git)
        for page in pages:
            await ctx.send(page)
        pass

    @git.command()
    @utils.is_bot_moderator
    async def merge(self, ctx: commands.Context, pr: int):
        """
        Merge a PR.
        """
        gh_token = getenv("GH_TOKEN")

        data = {
            "commit_title": f"#{pr} Merged by {ctx.message.author}",
            "commit_message": f"Merge triggered by command in #{ctx.channel.name}."
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {gh_token}"
        }

        await ctx.typing()
        async with aiohttp.ClientSession() as session:
            resp = await session.put(f"https://api.github.com/repos/general-programming/thonkbot/pulls/{pr}/merge",
                                     data=json.dumps(data), headers=headers)

            if resp.status == 200:
                await ctx.send(f"Merged #{pr} successfully.")
            else:
                body = await resp.json()
                await ctx.send(f"Merge failed:\n```\n{body['message']}\n```")

def setup(bot: commands.Bot):
    bot.add_cog(GitManagementCog())
