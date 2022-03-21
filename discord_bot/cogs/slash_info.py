from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

from functions import get_prefix, get_time

client = commands.Bot(command_prefix = get_prefix, Intents=intents)

class Slash(Cog):
    def __init__(self, client: Bot):
        self.client = client

    @cog_ext.cog_slash(name="test")
    async def _test(self, ctx: SlashContext):
        embed = Embed(title="Embed Test")
        await ctx.send(embed=embed)

def setup(client: client):
    client.add_cog(Slash(client))
