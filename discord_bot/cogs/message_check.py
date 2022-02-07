import discord, json, io, os, typing, requests, random, asyncio
import sys
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

tasks = {          # 'name' : [ 'ammount', 'max words count', 'name of column', 'name of required column' ]
	'key_words' : [ None, None, 'key_words_check', 'key_words' ],
	'set_key_words' : [ 6, 20, 'key_words', None ],
	'links' : [ None, None, 'link_check', None ]
	}

message_links = [] # defined when processing messages, stores links found in message
message_links_mark = {} # defined when processing urls in message, stroes information about each link

white_listed_links = [] # pre-defined links marked as a 100% legit no scam
black_listed_links = [] # pre-defined links marked as a hell in a link form
black_listed_words = [] # pre-defined words that are used in scam links

settings = { 'off' : 'NO', 'on' : 'YES', 'YES' : 'ON', 'NO' : 'OFF' } # This dictionary is only for saving YES/NO type information in to database, and converting it to/from nice 'ON' and 'OFF'

class Processing:
	
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
		
	@staticmethod
	async def msg_process_check(self, ctx, task, number : int, value):
		if ( not ctx.message.author.guild_permissions.administrator ): # Whell, it checks if caller has required permissions ( for setup commands it is ALWAYS administrator )
			raise MissingPermissions('You can not use this command')
		
		if task in tasks.keys():
			if not tasks[task][1]:
				if value != 'off' or value != 'on':
					raise commands.BadArgument(f'{task.capitalize()} require ON/OFF type value')
			if tasks[task][0]:
				if number > tasks[task][0] or number == 0:
					raise commands.BadArgument(f'{task.capitalize()} can set count to maximum {tasks[task][0]} and minimum 1')
			if tasks[task][1]:
				if value.split() > tasks[task][1]:
					raise commands.BadArgument(f'Maximum number of {task}s is {tasks[task][1]}')
			if tasks[task][3]:
				if get_database_data('servers_msg_process', tasks[task][3], ctx.guild.id):
					raise commands.BadArgument(f'You have to set {tasks[task][3]} before.')
			return 1
		else:
			raise commands.BadArgument(f'Unknown task {task}.')
	
	@staticmethod
	async def msg_process_execute(self, ctx, task, number : int, value):
		if value == 'off' or value == 'on':
			set_value = settings[value]
		column = tasks[task][2]
		write_database_data('servers_msg_process', column, ctx.guild.id, set_value)
		return f'Success! {task.capitalize()} has been set to {value.upper()}'
	
	@staticmethod
	async def check_for_urls(self, ctx):
		message_links = []
		if (('http://' in ctx.message.content ) or ('https://' in ctx.message.content)):
			for i in ctx.message.content.split():
				if  ( 'http://' in i ) or ( 'https://' in i ):
					message_links.append(i)
			return message_links
		else:
			return 0
	
	@staticmethod
	async def check_for_keys(self, ctx, guild_keys):
		message_keys = []
		for key in guild_keys:
			if ( key in ctx.message.content ):
				for i in ctx.message.content.split():
					if  ( key in i ):
						message_keys.append(i)
		return message_keys

	@staticmethod
	async def process_urls(self, ctx, message_urls):
		message_links_mark = {}
		for url in message_urls:
			message_links_mark[url] = 'whiteword'
			for white_link in white_listed_links: # check if link starts with whitelisted url
				if url.startswith(white_link):
					message_links_mark[url] = 'whitelink'
					continue
			for black_link in black_listed_links: # check if link starts with blacklisted url
				if url.startswith(black_link): 
					message_links_mark[url] = 'blacklink'
					continue
			for black_word in black_listed_words: # check if black listed word in link
				if black_word in url.content: 
					message_links_mark[url] = 'blackword'
					continue
		return message_links_mark

class Message_check(commands.Cog):
	def __init__(self, client):
		self.client = client
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Message check module loaded')
    
	async def cog_command_error(self, ctx, error):
		"""A local error handler for all errors arising from commands in this cog."""
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
			
		elif isinstance(error, commands.errors.ChannelNotFound):
			await ctx.channel.send("Channel not found!")
			
		elif isinstance(error, commands.BadArgument):
			await ctx.channel.send(error)
			
		elif isinstance(error, commands.MissingRequiredArgument):
			await ctx.channel.send(error)
			
		elif isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.send('This command can not be used in Private Messages.')
			except discord.HTTPException:
				pass
		else:
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
	@commands.command()
	async def msg_process(self, ctx, task, number : typing.Optional[int] = 0,  *, value):
		task = task.lower()
		value = value.lower()
		if Processing.msg_process_check(ctx, task, number, value):
			pass
		else:
			return 0
		returning_string = Processing.msg_process_execute(ctx, task, number, value)
		if returning_string:
			return await ctx.send(returning_string)
		else:
			pass
	
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
		modDeleted = False
		guild_id = message.guild.id
		database_record = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
		if database_record == None:
			return 0
		deleter = None
		if (message.author.bot):
			return 0
		if message.content.startswith('$say'):
			return 0
		async for entry in message.guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
			if entry.created_at.now() == datetime.utcnow():
				deleter = entry.user
				modDeleted = True
		channel = self.client.get_channel( id = database_record )
		embed = discord.Embed( 
			title="Message deleted",
			description="Deleted by moderator" if modDeleted else "Deleted by user",
			color= message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=deleter.icon_url if modDeleted else message.author.avatar_url)
		embed.add_field(name= chr(173), value=f"**Message author**: {message.author} \n**Message author ID**: {message.author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Deleter**: {deleter if modDeleted else message.author} \n**Deleter ID**: {deleter.id if modDeleted else message.author.id}", inline=True),
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
		if message_before.content == message_after.content:
			return 0
		channel = self.client.get_channel( id = database_record )
		embed = discord.Embed( 
			title="Message edited",
			description=" ",
			color= message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name= chr(173), value=f"**Message author**: {message.author} \n**Message author ID**: {message.author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
		embed.add_field(name= 'Message content before:', value=message_before.content, inline=False),
		embed.add_field(name= 'Message content after:', value=message_after.content, inline=False),
		embed.set_footer(text="Provided by Wild West Post Office")
		await channel.send(embed=embed)
		
def setup(client):
	client.add_cog(Message_check(client))
