from discord.ext import commands
from discord import Embed
import requests

class xkcd:
    @commands.command()
    async def xkcd(self, ctx, number = None):
        import calendar
        if number is None:
            data = requests.get("https://xkcd.com/info.0.json")
        else:
            data = requests.get(f"https://xkcd.com/{number}/info.0.json")
        body = data.json()
        e = Embed()
        e.description = f"[#{body['num']} - **{body['title']}**](https://xkcd.com/{body['num']})"
        e.set_image(url=body['img'])
        month = calendar.month_name[int(body['month'])]
        date = f"{body['day']} {month} {body['year']}"
        e.set_footer(text=f"{body['alt']} | {date}")
        await ctx.send(embed=e)


def setup(bot):
    bot.add_cog(xkcd())
