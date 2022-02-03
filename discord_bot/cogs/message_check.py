import discord, json, io, os, typing, requests, random, asyncio
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot

from functions import get_prefix, get_time, get_database_data

client = commands.Bot(command_prefix = get_prefix)

load_dotenv()

class Message_processing:
	
	def __init__(self, ctx):
		self.bot = ctx.bot
		self.client = ctx.client
		self._author = ctx.message.author
		self._authorId = ctx.message.author.id
		self._guild = ctx.guild
		self._guildId = ctx.guild.id
		self._channel = ctx.channel
		self._channelId = ctx.channel.id
		self._content = ctx.message.content
		self._wordList = ctx.message.content.split()
		
	@classmethod
	async def check_for_urls(self, ctx):
		pass
		

class Message_check(commands.Cog):
	def __init__(self, client):
		self.client = client
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Message check module loaded')
    
	@commands.Cog.listener()
	async def on_message(self, message):
		#await client.process_commands(message)
		guild_id = message.guild.id
		database_record = get_database_data('servers_properties', 'message_check_feature', guild_id)
		black_listed = ['Gift', 'gift', 'Steam', 'steam', 'Free', 'free', 'Nitro', 'nitro', 'Discord', 'discord', 'giveaway', 'Giveaway', 'Skin', 'skin', 'CS:GO', 'Counter-Strike: Global Offensive', 'CS']
		black_listed_length = (len(black_listed))
		black_listed_words_number_detected = 0
		if database_record == 'NO':
			return 0
		alert_channel_id = get_database_data('servers_data', 'message_check_channel_id', guild_id)
		alert_channel = self.client.get_channel( id = alert_channel_id )
		if (message.author == client.user):
			return 0
		if (('http://' in message.content ) or ('https://' in message.content)):
			for x in black_listed:
				if (x in message.content):
					black_listed_words_number_detected += 1
			if (black_listed_words_number_detected >= 2):
				message_state = 'Define'
				try:
					await message.delete()
					message_state = 'deleted'
					#print("Message deleted")
				except commands.errors.MessageNotFound:
					message_state = 'not found'
				except discord.Forbidden:
					message_state = 'not deleted due to not enough permissions'
				except:
					#print("Message not deleted")
					message_state = 'not deleted'
				print("\nPosible scam by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} \". Message {}.".format(message.author, message.channel, message.guild, get_time(), message_state))
				message_state = message_state.capitalize()
				message_content = ('`' + message.content + '`')
				message_words = []
				message_words = message.content.split() 
				link = []
				nolinks = 0
				for i in message_words:
					if  ( 'http://' in i ) or ( 'https://' in i ):
						nolinks = nolinks + 1
						link.append('||`' + i + '`||')
						#print(f"link0: {link}")
				embed = discord.Embed( 
					title="Message flagged",
					description=" ",
					color=0x0000ff,
					timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
				)
				embed.add_field(name= chr(173), value=f"**User**: {message.author} \n**User ID**: {message.author.id}", inline=True),
				embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
				embed.add_field(name= chr(173), value=chr(173), inline=False),
				embed.add_field(name="Message content:", value=message_content, inline=True),
				if nolinks == 1:
					embed.add_field(name="Link:", value=link[0], inline=True),
				else:
					links = ''.join(str(x + ' | ') for x in link)
					links = links[:-2]
					embed.add_field(name="Links:", value=links, inline=True),
				embed.add_field(name=chr(173), value=f"**Message status**: {message_state}", inline=False),
				embed.set_footer(text="Provided by Wild West Post Office")
				await alert_channel.send(embed=embed)
		else: 
			return 0
		
	@commands.Cog.listener()
	async def on_message_delete(self, message):
		#print("Message deleted")
		guild_id = message.guild.id
		database_record = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
		if database_record == None:
			return 0
		async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
        		deleter = entry.user
		channel = self.client.get_channel( id = database_record )
		embed = discord.Embed( 
			title="Message deleted",
			description=" ",
			color= message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=deleter.icon_url)
		embed.add_field(name= chr(173), value=f"**Message author**: {message.author} \n**Message author ID**: {message.author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Deleter**: {deleter} \n**Deleter ID**: {deleter.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
		embed.add_field(name= 'Message content:', value=message.content, inline=True),
		embed.set_footer(text="Provided by Wild West Post Office")
		await channel.send(embed=embed)
		
	@commands.Cog.listener()
	async def on_message_edit(self,message_before, message_after):
		message = message_after
		guild_id = message.guild.id
		database_record = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
		if database_record == None:
			return 0
		channel = self.client.get_channel( id = database_record )
		embed = discord.Embed( 
			title="Message edited",
			description=" ",
			color= message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=message.author.icon_url)
		embed.add_field(name= chr(173), value=f"**Message author**: {message.author} \n**Message author ID**: {message.author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
		embed.add_field(name= 'Message content before:', value=message_before.content, inline=False),
		embed.add_field(name= 'Message content after:', value=message_after.content, inline=False),
		embed.set_footer(text="Provided by Wild West Post Office")
		await channel.send(embed=embed)
		
def setup(client):
	client.add_cog(Message_check(client))
