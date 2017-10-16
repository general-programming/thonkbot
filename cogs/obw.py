from discord.ext import commands
import discord
import re
import random

class Obw:
    """
    Obw's cog
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

def setup(bot: commands.Bot):
    bot.add_cog(Obw())
