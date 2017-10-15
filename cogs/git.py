from discord.ext import commands
from os import getenv
import aiohttp

class GitManagementCog:
    def __init__(self):
        pass

    async def __local_check(self, ctx: commands.Context):
        return True

    @commands.command()
    async def gitmerge(self, ctx: commands.Context, pr: int):
        """
        Merge a PR.
        """
        gh_token = getenv("GH_TOKEN")

        data = {
            "commit_title": f"Merged by {ctx.message.author}",
            "commit_message": f"Merge triggered by command in #{ctx.channel.name}."
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"token {gh_token}"
        }

        async with aiohttp.ClientSession() as session:
            resp = await session.put(f"https://api.github.com/repos/general-programming/thonkbot/pulls/{pr}/merge",
                                     data=data, headers=headers)

            if resp.status == 200:
                await ctx.send(f"Merged #{pr} successfully.")
            else:
                body = await resp.json()
                await ctx.send(f"Merge failed:\n```\n{body['message']}\n```")

def setup(bot: commands.Bot):
    bot.add_cog(GitManagementCog())
