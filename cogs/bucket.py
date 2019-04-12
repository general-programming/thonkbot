from discord.ext import commands
from thonk import utils
import re


class Bucket(commands.Cog):
    patterns = {}

    def __init__(self, bot):
        self.patterns = utils.load_json('data/bucket.json')
        self.bot = bot

    def process(self, match, res):
        if match.lastindex:
            for i in range(0, match.lastindex + 1):
                res = res.replace(f'${i}', match.group(i))

        return res

    async def on_message(self, msg):
        if msg.channel.id != 321039517136060418:
            return

        if msg.author.id == self.bot.user.id:
            return

        if msg.content.startswith(tuple(self.bot.command_prefix)):
            return

        for p in self.patterns:
            match = re.search(p, msg.content, re.I)
            if match is not None:
                await msg.channel.send(self.process(match, self.patterns[p]))

    @commands.command()
    async def blist(self, ctx):
        patterns = '\n'.join([k + " = " + v for k, v in self.patterns.items()])
        await ctx.send(f"```\n{patterns}```")

    @commands.command()
    async def bsave(self, ctx):
        utils.dump_json(self.patterns, "data/bucket.json")

    @commands.command(aliases=['b'])
    async def bucket(self, ctx, *, msg):

        match = re.match(r'(?P<subject>.+)(?P<verb>\s+is\s+|\s+are\s+|<.+>)(?P<object>.+)', msg, re.I)
        if match is not None:
            groups = match.groupdict()
            subject = groups['subject'].strip()
            verb = groups['verb'].strip()
            sobject = groups['object'].strip()

            if verb[0] == '<' and verb[-1:] == '>':
                if verb == "<'s>":
                    self.patterns[subject] = p = f"{subject}'s {sobject}"
                elif verb == '<reply>':
                    self.patterns[subject] = p = f"{sobject}"
                elif verb == '<action>':
                    self.patterns[subject] = p = f"*{sobject}*"
                else:
                    self.patterns[subject] = p = f"{subject} {verb[1:-1]} {sobject}"
            else:
                self.patterns[subject] = p = f"{subject} {verb} {sobject}"

            await ctx.send(f"```{p}```")
        else:
            await ctx.send("Your message did not match.")


def setup(bot: commands.Bot):
    bot.add_cog(Bucket(bot))
