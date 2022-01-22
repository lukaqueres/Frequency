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
	async def info(self, ctx, value = 'default', secondary_value : discord.Member=None):
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
      
		embed.add_field( name="Name", value=str(user), inline=True),
		embed.add_field( name="ID", value=user.id, inline=True),
		embed.add_field( name="Bot?", value=user.bot, inline=True),
		embed.add_field( name="Top role", value=user.top_role.mention, inline=True),
		embed.add_field( name="Status", value=str(user.status).title(), inline=True),
		embed.add_field( name="Activity", value=f"{str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}", inline=True),
		embed.add_field( name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True),
		embed.add_field( name="Joined at", value=user.joined_at.strftime("%d/%m/%Y %H:%M:%S"), inline=True),
		embed.add_field( name="Boosted", value=bool(user.premium_since), inline=True)

		await ctx.send(embed=embed)
    
def setup(client):
	client.add_cog(Information(client))
