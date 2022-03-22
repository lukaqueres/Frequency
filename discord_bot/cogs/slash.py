import discord, json, io, os, typing, requests, random, asyncio
from discord import member, DMChannel, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option

from functions import get_prefix, get_time, get_guilds_ids

intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, Intents=intents)

slash = SlashCommand(client, sync_commands=True)

guild_ids = get_guilds_ids()

async def commands_modules():
	return ["test","tust","tast","tist"]

class Slash(Cog):
	def __init__(self, client: Bot):
		self.client = client
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Slash commands module loaded')
    
	@cog_ext.cog_slash(name="clear", 
	                   description="Delets messages by number or filter", 
	                   guild_ids=guild_ids,
	                   options=[
				   create_option(
                                	name = "ammount",
                                	description = "Restrict maximum number of messages to delete",
                                	option_type = 4,
                                	required = False
                               	   ),
				   create_option(
                                	name = "user",
                                	description = "Restrict by message author",
                                	option_type = 6,
                                	required = False
                               	   )
			   	   ])
	@commands.has_permissions(manage_messages=True)
	async def _clear(ctx: SlashContext, ammount: int, user = None): 
		if number =< 0:
			return await ctx.send(">>> Invalid number given", hidden=True)
		embed = Embed(title="Embed Test")
		await ctx.send(f"No {ammount or 0 } by user {user or 'NO'}", hidden=True)
        
	@cog_ext.cog_slash(name="help", 
				guild_ids=guild_ids, 
				description="Provides information about bot itself or specific commands",
                       options=[create_option(
                                   name = "command",
                                   description = "What command do you want learn more about?",
                                   option_type = 3,
                                   required = False
                                ),
                                create_option(
                                   name = "module",
                                   description = "What commands do you want to check?",
                                   option_type = 3,
                                   required = False
                                )])
	async def _help(self, ctx: SlashContext, command = None, module = None):
		if not ctx.author.guild_permissions.manage_messages:
			return await ctx.send(">>> You can't use this!", hidden=True)
		embed = Embed(title="Embed Test")
		await ctx.send(embed=embed, hidden=True)

def setup(client: client):
	client.add_cog(Slash(client))
