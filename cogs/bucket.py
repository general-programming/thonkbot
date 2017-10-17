from discord.ext import commands
from thonk import utils
import re
import json


class Bucket:

    patterns = {}

    def __init__(self, bot):
        self.patterns = utils.load_json('data/bucket.json')
        self.bot = bot

    def process(self, msg, str, match=None):
        str = str.replace('$who', msg.author.mention)

        if match is None:
            str = str.replace('$noun', r'(.+)')
        else:
            if match.lastindex is not None and match.lastindex > 0:
                word = match.group(1)
                str = str.replace('$noun', match.group(1))
        return str

    async def on_message(self, msg):
        if msg.channel.id != 321039517136060418:
            return

        if msg.author.id == self.bot.user.id:
            return

        if msg.content.startswith(tuple(self.bot.command_prefix)):
            return

        for p in self.patterns:
            match = re.search(self.process(msg, p), msg.content, re.I)
            if match is not None:
                await msg.channel.send(self.process(msg, self.patterns[p], match))

    @commands.command()
    async def bdebug(self, ctx):
        patterns = '\n'.join(self.patterns.keys())
        await ctx.send(f"```\n{patterns}```")

    @commands.command()
    async def bsave(self, ctx):
        with open('bucket.json', 'w') as outfile:
            json.dump(self.patterns, outfile)


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


            return

        else:
            await ctx.send("Your message did not match.")

def setup(bot: commands.Bot):
    bot.add_cog(Bucket(bot))
