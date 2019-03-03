from thonk import utils
from discord.ext import commands
from discord.ext.commands.bot import _mention_pattern, _mentions_transforms

@commands.command(name='help')
async def _help(ctx, *commands: str):
    """Shows this message."""
    bot = ctx.bot
    destination = ctx.message.author if bot.pm_help else ctx.message.channel

    def repl(obj):
        return _mentions_transforms.get(obj.group(0), '')

    # help by itself just lists our own commands.
    if len(commands) == 0:
        pages = await bot.formatter.format_help_for(ctx, bot)
    elif len(commands) == 1:
        # try to see if it is a cog name
        name = _mention_pattern.sub(repl, commands[0])
        command = None
        if name in bot.cogs:
            command = bot.cogs[name]
        else:
            for cog in bot.cogs:
                if name == utils.cog_get_pretty_name(bot.cogs[cog]):
                    command = bot.cogs[cog]
                    name = cog
                    break

        if command is None:
            command = bot.all_commands.get(name)
            if command is None:
                await destination.send(bot.command_not_found.format(name))
                return

        pages = await bot.formatter.format_help_for(ctx, command)
    else:
        name = _mention_pattern.sub(repl, commands[0])
        command = bot.all_commands.get(name)
        if command is None:
            await destination.send(bot.command_not_found.format(name))
            return

        for key in commands[1:]:
            try:
                key = _mention_pattern.sub(repl, key)
                command = command.all_commands.get(key)
                if command is None:
                    await destination.send(bot.command_not_found.format(key))
                    return
            except AttributeError:
                await destination.send(bot.command_has_no_subcommands.format(command, key))
                return

        pages = await bot.formatter.format_help_for(ctx, command)

    if bot.pm_help is None:
        characters = sum(map(lambda l: len(l), pages))
        # modify destination based on length of pages.
        if characters > 1000:
            destination = ctx.message.author

    for page in pages:
        await destination.send(page)

def setup(bot):
    bot.remove_command('help')
    bot.add_command(_help)
