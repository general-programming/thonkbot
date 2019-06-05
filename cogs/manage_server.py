from discord import VoiceRegion, Embed, Color
from discord.ext import commands
from discord.ext.commands import Bot, Cog, Context, Converter
from thonk.utils import require_tag

class VoiceRegionConverter(Converter):
    async def convert(self, ctx: Context, argument: str):
        return VoiceRegion(argument)

class ServerManagementCog(Cog):
    @commands.command()
    @require_tag("member")
    async def switch_region(self, ctx: Context, new_region: VoiceRegionConverter):
        """Change the server voice region."""

        await ctx.guild.edit(reason=f"Switch region command triggered by {ctx.author}", region=new_region)
        await ctx.send(embed=Embed(title=f"\N{WHITE HEAVY CHECK MARK} Updated voice region to {new_region}.",
                                   color=Color.gold())
                       )

def setup(bot: Bot):
    bot.add_cog(ServerManagementCog())
