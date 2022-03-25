import discord, json, io, os, typing, requests, random, asyncio
from discord import member, DMChannel, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import has_permissions, MissingPermissions

from datetime import datetime, date, timedelta
from functions import get_prefix, get_time, get_guilds_ids

intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, Intents=intents)

#slash = SlashCommand(client, sync_commands=True)

guild_ids = get_guilds_ids()

class Slash_music(Cog):
	def __init__(self, client: Bot):
		self.client = client
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Slash music module loaded')
    
def setup(client: client):
	client.add_cog(Slash_music(client))
