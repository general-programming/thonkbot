from discord.ext.commands import Bot, Cog, Context, group, command
from discord import Embed, Color
from consul.aio import Consul
from enum import Enum

class ThonkOpsCog(Cog):
    def __init__(self):
        self.consul = Consul(host='localhost', port=8500)

    @group()
    async def consul(self, ctx: Context):
        pass

    @consul.command()
    async def services(self, ctx: Context):
        """List consul services"""
        embed = Embed(title="Consul Services", color=Color.orange())

        index, node = await self.consul.catalog.services()

        for name, tags in node.items():
            traefik_enabled = 'traefik.enable=true' in tags

            embed.add_field(name=name, value="Traefik enabled" if traefik_enabled else "\u200b")

        await ctx.send(embed=embed)

    @consul.command()
    async def service(self, ctx: Context, service_name: str):
        """Show information about a Consul service"""
        index, nodes = await self.consul.catalog.service(service_name)

        if len(nodes) == 0:
            return await ctx.send(f"\N{NO ENTRY SIGN} Service `{service_name}` not found!")

        service = nodes[0]
        embed = Embed(title=service["ServiceName"], color=Color.orange())
        embed.add_field(name="Address", value=f"{service['Address']}:{service['ServicePort']}")
        embed.add_field(name="Nodes", value=", ".join(map(lambda n: n["Node"], nodes)))

        await ctx.send(embed=embed)

    class ConsulStatus(Enum):
        Unknown = 0
        Alive = 1
        Leaving = 2
        Left = 3
        Failed = 4

        def __str__(self):
            return self.name

    @consul.command()
    async def members(self, ctx: Context):
        """List Consul cluster members"""

        embed = Embed(title="Consul cluster members", color=Color.orange())
        members = await self.consul.agent.members()

        for member in members:
            embed.add_field(name=f"{member['Name']} ({self.ConsulStatus(member['Status'])})", value=member['Addr'])

        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog(ThonkOpsCog())
