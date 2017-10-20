from discord.ext import commands
from thonk import twitter, utils
import discord
import re
import random

async def find_last_user_message(ctx: commands.Context, user: discord.User) -> discord.Message:
    async for msg in ctx.channel.history(before=ctx.message):
        if msg.author.id == user.id:
            return msg

class Obw:
    """
    obw's cog
    """
    DIE_REGEX = re.compile(r"(\d+)d(\d+)(?:\+(\d+))?", re.IGNORECASE)

    def __init__(self):
        pass

    def parse_die(self, die: str):
        parts = self.DIE_REGEX.match(die)

        if parts is None:
            raise commands.BadArgument("Incorrect dice format! Format: `<number of dice>d<max>(+<offset>)")

        n, v = map(int, parts.group(1, 2))
        offset = int(parts.group(3) or 0)

        if n > 50:
            raise commands.BadArgument("I can't roll that many dice!")
        if v > 10000:
            raise commands.BadArgument("That's a bit of a large die...")

        rolls = map(lambda i: str(random.randint(offset, v + offset)), range(0, n))
        return list(rolls)

    @commands.command()
    async def roll(self, ctx: commands.Context, *dice: str):
        """
        Roll dice!
        """
        embed = discord.Embed(title="Dice Roll Results")

        for die in dice:
            rolls = self.parse_die(die)
            embed.add_field(name=die, value=", ".join(rolls))

        await ctx.send(embed=embed)

    @commands.command()
    async def flip(self, ctx: commands.Context, *, to_flip: str):
        parts = map(lambda s: s.trim(), to_flip.split(","))
        picked = random.choice(parts)

        await ctx.send(picked)

    @commands.command()
    async def quote(self, ctx: commands.Context, *, username: str):
        """
        Tweet a quote of <username>'s last message.
        """
        try:
            user = await commands.MemberConverter().convert(ctx, username)
        except commands.BadArgument:
            user = discord.utils.find(lambda u: u.name.lower().startswith(username.lower()), ctx.guild.members)

        if user is None:
            return await ctx.send("Couldn't find that user to quote!")

        msg = await find_last_user_message(ctx, user)
        tweet_text = f"\"{msg.clean_content}\" - {str(msg.author)}"
        media = []

        if len(msg.attachments) > 0:
            for attachment in msg.attachments:
                res = await twitter.upload(await utils.to_fp(attachment))
                media.append(res.media_id)

        if len(msg.clean_content) == 0:
            raise commands.CommandError("That message is empty!")

        if len(tweet_text) > 140:
            raise commands.CommandError("Quote is too long to be a tweet!")

        tweet = await twitter.tweet(tweet_text, media_ids=media)
        await ctx.send(f"https://twitter.com/{tweet.user['screen_name']}/status/{tweet.id_str}")

def setup(bot: commands.Bot):
    bot.add_cog(Obw())
