import discord, json, io, os, typing, requests, random, asyncio, psycopg2
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, Embed, Intents
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot
from typing import Optional

from functions import get_prefix, get_time, get_database_data

intents = discord.Intents.all()
intents.presences = True
intents.members = True
intents.guilds = True
intents.messages = True
client = commands.Bot(command_prefix = get_prefix, Intents=intents)

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()
"""
#(ctx, user: typing.Optional[discord.Member] = None, *, guild: discord.Guild = None)
class Extract: 
	def __init__(self, ctx, user: typing.Optional[discord.Member] = None, *, guild: discord.Guild = None):
		object_type = user or guild
		rolelist = [r.name for r in object_type.roles if r != ctx.guild.default_role] #or [r.name for r in guild.roles if r != ctx.guild.default_role]
		roles = " | ".join(reversed(rolelist))
		defines = [( '_name', object_type ),
			   ( '_id', object_type.id ),
			   ( '_created', object_type.created_at.strftime("%d/%m/%Y %H:%M:%S") ),
			   ( '_joined', user.joined_at.strftime("%d/%m/%Y %H:%M:%S") or None ),
			   ( '_roles', roles ),
			   ( '_status', str(user.status).title() or None ),
			   ( '_activity', (str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A') + (user.activity.name if user.activity else '') or None ),
			   ( '_isBot', ('NO' if not user.bot else 'YES') or None ),
			   ( '_topRole', user.top_role.name or None ),
			   ( '_numOfRoles', len(rolelist) ),
			   ( '_hasNitro', ('Yes' if bool(user.premium_since) else 'No') or None ),
			   ( '_owner', (guild.owner or None) ),
			   ( '_numOfLives', (len([m for m in guild.members if not m.bot])) or None ),
			   ( '_numOfBots', len([m for m in guild.members if m.bot]) or None ),
			   ( '_numOfTxtChannels', len([x for x in guild.channels if type(x) == discord.channel.TextChannel]) or None ),
			   ( '_numOfRoles', len(guild.roles) or None ),
			   ( '_numOfEmois', len(guild.emojis) or None ),
			   ( '_verLevel', str(guild.verification_level) or None ),
			   ( '_highestRole', guild.role_hierarchy[0] or None )]
					
		self.client = client
		for name, value in defines:
			try:
				setattr(self, name, value)
			except:
				print(f"Failed: {name}")"""

class Information(commands.Cog):
	"""Commands for getting various information"""
	def __init__(self, client):
  		self.client = client
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Information module loaded')

	@commands.command(name='info', usage='info < user/server > [ member ]', brief='Displays many useful information about guild', description='xd')
	async def info(self, ctx, value = 'default', member : discord.Member=None): # secondary_value : discord.Member=None <- for specified type of input
		if value == 'default': # You can't pick nothin' do ya? 
			await ctx.send("You have to specify what kind of information you want!")
			return 0
		if value == 'user': # If user type information picked
			if (member != None) and (member != ctx.message.author):
				if ( not ctx.message.author.guild_permissions.manage_roles): # Check if user have permissions to show info about other user
					await ctx.send("You can't check info about other user than you!")
					return 0
			
			user = member or ctx.author
			#_user = Extract(ctx, user)
			rolelist = [r.name for r in user.roles if r != ctx.guild.default_role]
			roles = " | ".join(reversed(rolelist))
			#print(f"status: {user.status}, activity: {user.activity.type if user.activity else 'N/A'}")
			account_created = user.created_at.strftime("%d/%m/%Y %H:%M:%S")
			guild_join = user.joined_at.strftime("%d/%m/%Y %H:%M:%S")
			embed = Embed(title="User information",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=user.avatar_url)
      
			embed.add_field( name=chr(173), value=f"**User**: {str(user)}\n**User ID**: {user.id}", inline=True),
			embed.add_field( name=chr(173), value=f"**Created**: {account_created}\n**Joined**: {guild_join}", inline=True),
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			embed.add_field( name="All roles:", value=roles, inline=False),
			embed.add_field(name = chr(173), value = f"**Status**: {str(user.status).title()}\n**Activity**: {str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}\n**Bot**: {'NO' if not user.bot else 'YES'}", inline=True),
			embed.add_field( name= chr(173), value=f"**Top role**: {user.top_role.name}\n**Number of roles**: {len(rolelist)}\n**Nitro**: { 'Yes' if bool(user.premium_since) else 'No'}", inline=True),
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			#embed.add_field( name="Bot:", value=user.bot, inline=True),
			#embed.add_field( name="Status", value=str(user.status).title(), inline=True), <- FIX IT
			#embed.add_field( name="Activity", value=f"{str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}", inline=True), <- FIX IT
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			#embed.add_field( name="Created at:", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True),
			#embed.add_field( name="Joined at:", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True),
			#embed.add_field( name="Boosted:", value=bool(user.premium_since), inline=True)
			embed.set_footer(text="Provided by Wild West Post Office")

			await ctx.send(embed=embed)
		if (value == 'server') or (value == 'guild'):
			guild = ctx.guild
			#_guild = Extract(ctx, guild)
			live_members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots 
			bot_members_count = len([m for m in guild.members if m.bot]) # only bots 
			rolelist = [r.name for r in guild.roles if r != ctx.guild.default_role]
			roles = " | ".join(reversed(rolelist))
			users_online = 0
			for i in guild.members:
				if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
					users_online += 1

			channels_number = len([x for x in guild.channels if type(x) == discord.channel.TextChannel])

			roles_number = len(guild.roles)
			emojis_number = len(guild.emojis)
			created_at = guild.created_at.strftime("%d/%m/%Y %H:%M:%S")
			
			embed = Embed(title="Server information",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=guild.icon_url)
			
			embed.add_field(name=chr(173), value=f"**Guld name**: {guild.name}\n**Guild ID**: {guild.id}\n**Guild owner**: {guild.owner}", inline=True)
			#embed.add_field(name='Owner:', value=guild.owner)
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			embed.add_field(name=chr(173), value=f"**Members**: {guild.member_count}\n**Users**: {live_members_count}\n**Bots**: {bot_members_count}", inline=True)
			#embed.add_field(name='Users:', value=live_members_count)
			#embed.add_field(name='Bots:', value=bot_members_count)
			embed.add_field(name='Server roles:', value=roles, inline=False)
			#embed.add_field(name='Currently Online:', value=users_online) <- FIX IT
			embed.add_field(name=chr(173), value=f"**Number of text channels**: {str(channels_number)}\n**Number of roles**: {str(roles_number)}\n**Number of emotes**: {str(emojis_number)}", inline=True)
			#embed.add_field(name='Region:', value=guild.region)
			embed.add_field(name=chr(173), value=f"**Veryfication level**: {str(guild.verification_level)}\n**Created**:{created_at}", inline=True)
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			#embed.add_field(name='Highest role:', value=guild.role_hierarchy[0]) <- FIX IT
			#embed.add_field(name='Number of roles:', value=str(roles_number))
			#embed.add_field(name='Number of emotes:', value=str(emojis_number))
			#embed.add_field(name='Created At:', value=guild.created_at.strftime("%d/%m/%Y %H:%M:%S") #.__format__('%A, %d. %B %Y %H:%M:%S'))
			embed.set_footer(text="Provided by Wild West Post Office")
			await ctx.send(embed=embed)
		
	@info.error
	async def info_error(self, ctx: commands.Context, error):
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
		else: 
			print(error)
			await ctx.channel.send("There was an error with executing command!")

def setup(client):
	client.add_cog(Information(client))
