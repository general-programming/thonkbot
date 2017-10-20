from discord.ext import commands
from raven import Client
from thonk import utils
from thonk.sentry import AioHttpTransport
import traceback
import asyncio
import time

class Core:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._last_result = None

        if utils.is_deployed(bot):
            self.raven = Client(transport=AioHttpTransport)

    async def on_ready(self):
        print(f"Logged in as {self.bot.user.name}.")

    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.CommandInvokeError):
            if hasattr(self, "raven"):
                self.raven.captureException(exc_info=utils.exc_info(error.original))
            error = error.original

        if not utils.is_deployed(ctx.bot):
            traceback.print_exception(*utils.exc_info(error))

        await ctx.send("💢 There was a problem!\n```\n" + utils.safe_text(str(error)) + "\n```")



    @commands.command()
    async def ping(self, ctx):
        """Pong!"""
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        diff = round((t2-t1)*1000)
        await ctx.send(f"Pong! {diff}ms")



    @commands.command()
    async def cogs(self, ctx):
        """
        Lists all cogs.
        """
        cogs = '\n'.join(map(utils.cog_get_pretty_name, ctx.bot.cogs.values()))
        await ctx.send(f"```\n{cogs}```")

    @commands.command()
    async def extensions(self, ctx):
        """
        Lists all extensions.
        """
        extensions = '\n'.join(ctx.bot.extensions.keys())
        await ctx.send(f"```\n{extensions}```")



    @commands.command()
    async def echo(self, ctx, *, arg):
        """
        Echos a raw message.
        """
        await ctx.send(arg)



    def remove_code_tags(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name="eval", hidden=True)
    @utils.require_tag('owner')
    async def _eval(self, ctx, *, body: str):
        """
        Evaluates python code.
        """
        import textwrap, io
        from contextlib import redirect_stdout

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
        env.update(globals())

        stdout = io.StringIO()

        body = self.remove_code_tags(body)

        executor = exec
        # single statement, try 'eval' mode
        if body.count('\n') == 0:
            try:
                code = compile(body, '<string>', 'eval')
            except SyntaxError:
                pass
            else:
                executor = eval

        # if we didn't try eval mode or it failed
        # then try exec mode
        if executor is exec:
            try:
                body = textwrap.indent(body, "  ")
                body = f"async def func():\n{body}\n"
                code = compile(body, '<string>', 'exec')
            except Exception as e:
                return await ctx.send(f'❌ There was a compiler error!```py\n{e.__class__.__name__}: {e}\n```')

        try:
            #await ctx.send(f'Source:```py\n{body}\n```')
            with redirect_stdout(stdout):
                ret = executor(code, env)
                if executor is exec: ret = await env['func']()
        except Exception as e:
            return await ctx.send(f'‼️ There was a runtime error!```py\n{e.__class__.__name__}: {e}\n```')

        #await ctx.send(f"Mode: `{executor.__name__}`")
        output = stdout.getvalue()
        if output:
            await ctx.send(f'Output:```py\n{output}\n```')
        if ret:
            await ctx.send(f'Returned:```py\n{ret}\n```')
        if not ret and not output:
            await ctx.message.add_reaction("✅")



    @commands.command()
    @utils.is_bot_moderator
    async def restart(self, ctx: commands.Context):
        """
        Restart the bot.
        """
        await ctx.send("Going down!")
        await self.bot.logout()

def setup(bot: commands.Bot):
    bot.add_cog(Core(bot))
