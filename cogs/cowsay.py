from discord.ext import commands
from itertools import zip_longest

cow = r"""
        \   ^__^
         \  ({0})\_______
            (__)\       )\/\
             {1}  ||----w |
                ||     ||
"""
modes = {
    '-b': '==',
    '-d': ('XX', 'U'),
    '-g': '$$',
    '-p': '@@',
    '-s': '**',
    '-t': '--',
    '-w': 'OO',
    '-y': '..',
}

class Cowsay(commands.Cog):
    """cowsay"""
    @commands.command()
    async def cowsay(self, ctx, opt, *, text = ''):
        """Cowsays a message."""

        msg = ''
        eyes = 'oo'
        tongue = ' '

        if opt in modes:
            if type(modes[opt]) is tuple:
                eyes, tongue = modes[opt]
            else:
                eyes = modes[opt]
        else:
            text = (opt + ' ' + text).strip()

        lines = text.splitlines()
        width = len(max(lines, key=len))
        height = len(lines)

        msg += ' _' + ('_' * width) + '_ \n'
        if height == 1:
            msg += f'< {lines[0]} >\n'
        else:
            lines = [l.strip().ljust(width) for l in lines]
            msg += f'/ {lines[0]} \\\n'
            for l in lines[1:-1]:
                msg += f'| {l} |\n'
            msg += f'\\ {lines[height-1]} /\n'
        msg += ' ‾' + ('‾' * width) + '‾ '

        msg += cow.format(eyes, tongue)

        await ctx.send(f'```{msg}```')
        return


def setup(bot):
    bot.add_cog(Cowsay())
