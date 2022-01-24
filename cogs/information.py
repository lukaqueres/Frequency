import discord, json, io, os, typing, requests, random, asyncio, psycopg2
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, Embed
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot
from typing import Optional

from functions import get_prefix, get_time

client = commands.Bot(command_prefix = get_prefix, intents=discord.Intents.all())

load_dotenv()

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

class Information(commands.Cog):
	def __init__(self, client):
  		self.client = client
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Information module loaded')

	@commands.command()
	async def info(self, ctx, value = 'default', secondary_value : discord.Member=None): # secondary_value : discord.Member=None <- for specified type of input
		if value == 'default': # You can't pick nothin' do ya? 
			await ctx.send("You have to specify what kind of information you want!")
			return 0
		if value == 'user': # If user type information picked
			if (secondary_value != None) and (secondary_value != ctx.message.author):
				if ( not ctx.message.author.guild_permissions.manage_roles): # Check if user have permissions to show info about other user
					await ctx.send("You can't check info about other user than you!")
					return 0
			if (secondary_value != None):
				user = secondary_value
			else:
				user = ctx.author
      
			embed = Embed(title="User information",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=user.avatar_url)
      
			embed.add_field( name="Name:", value=str(user), inline=True),
			embed.add_field( name="ID:", value=user.id, inline=True),
			embed.add_field( name="Bot:", value=user.bot, inline=False),
			embed.add_field( name="Top role:", value=user.top_role.mention, inline=True),
			#embed.add_field( name="Status", value=str(user.status).title(), inline=True), <- FIX IT
			#embed.add_field( name="Activity", value=f"{str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}", inline=True), <- FIX IT
			embed.add_field( name="Created at:", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False),
			embed.add_field( name="Joined at:", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True),
			embed.add_field( name="Boosted:", value=bool(user.premium_since), inline=True)

			await ctx.send(embed=embed)
		if value == 'server':
			live_members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots 
			bot_members_count = len([m for m in guild.members if m.bot]) # only bots 
			guild = ctx.guild
			users_online = 0
            		for i in guild.members:
                		if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                    			users_online += 1

            		channels_number = len([x for x in server.channels if type(x) == discord.channel.TextChannel])

            		roles_number = len(server.roles)
            		emojis_number = len(server.emojis)
			
			embed = Embed(title="Server information",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=guild.icon_url)
			
                	embed.add_field(name='Guild Name:', value=guild.name)
                	embed.add_field(name='Owner:', value=guild.owner, inline=False)
                	embed.add_field(name='Members:', value=guild.member_count)
			embed.add_field(name='Users:', value=live_members_count)
			embed.add_field(name='Bots:', value=bot_members_count)
                	embed.add_field(name='Currently Online', value=users_online)
                	embed.add_field(name='Text Channels', value=str(channels_number))
                	embed.add_field(name='Region', value=guild.region)
                	embed.add_field(name='Verification Level', value=str(guild.verification_level))
                	embed.add_field(name='Highest role', value=guild.role_hierarchy[0])
                	embed.add_field(name='Number of roles', value=str(roles_number))
                	embed.add_field(name='Number of emotes', value=str(emojis_number))
                	embed.add_field(name='Created At:', value=guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
                	embed.set_footer(text='Server ID: %s' % guild.id)
			
                	await ctx.send(embed=embed)
		
	"""@info.error
	async def info_error(self, ctx: commands.Context, error):
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
		else: 
			await ctx.channel.send("There was an error with executing command!")"""
    
def setup(client):
	client.add_cog(Information(client))
