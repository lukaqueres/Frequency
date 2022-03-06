import discord, json, io, os, typing, requests, random, asyncio
import sys
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

from functions import get_prefix, get_time, get_database_data, write_database_data

client = commands.Bot(command_prefix = get_prefix)

load_dotenv()

tasks = {          # 'name' : [ 'ammount', 'max words count', 'name of column', 'name of required column' ]
	'key_words' : [ None, None, 'key_words_check', 'key_words' ],
	'set_key_words' : [ None, 20, 'key_words', None ],
	'links' : [ None, None, 'link_check', None ],
	'set_key_words_limit' : [ None, 6, 'key_words_limit', None ],
	}

message_links = [] # defined when processing messages, stores links found in message
message_links_mark = {} # defined when processing urls in message, stroes information about each link

white_listed_links = [] # pre-defined links marked as a 100% legit no scam
black_listed_links = [] # pre-defined links marked as a hell in a link form
black_listed_words = [] # pre-defined words that are used in scam links

message_penalties = [ 'delete', 'pass' ]
user_penalties = [ 'ban', 'kick', 'pass' ]

settings = { 'off' : 'NO', 'on' : 'YES', 'YES' : 'ON', 'NO' : 'OFF' } # This dictionary is only for saving YES/NO type information in to database, and converting it to/from nice 'ON' and 'OFF'

class Processing:
	
	def __init__(self, ctx):
		self.bot = ctx.bot
		self.client = ctx.client
		self._author = ctx.message.author
		self._guild = ctx.guild
		self._channel = ctx.channel
		self._content = ctx.message.content
		self._wordList = ctx.message.content.split()
	
	@staticmethod
	async def check_for_urls(message):
		message_links = []
		if (('http://' in message.content ) or ('https://' in message.content)):
			for i in message.content.split():
				if  ( 'http://' in i ) or ( 'https://' in i ):
					message_links.append(i)
			return message_links
		else:
			return False
	
	@staticmethod
	async def check_for_keys(message, guild_keys):
		message_keys = []
		for key in guild_keys:
			if ( key in ctx.message.content ):
				for i in ctx.message.content.split():
					if  ( key in i ):
						message_keys.append(i)
		return message_keys

	@staticmethod
	async def process_urls(message, message_urls):
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
    
	"""async def cog_command_error(self, ctx, error):
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
			print('Ignoring exception in command {}:'.format(ctx.command))
			print(error)"""
	
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def key_words(self, ctx, task, number : typing.Optional[int] = 0,  *, key_value: typing.Optional[str] = None):
		if task:
			task = task.lower()
		if key_value:
			key_value = key_value.lower()
		if task == 'on' or task == 'off':
			if task == 'on':
				value = 'YES'
			else:
				value = 'NO'
			write_database_data('servers_msg_process', 'key_words_check', ctx.guild.id, value)
			return await ctx.send(f"Key word check set to {task}")
		if task == 'set':
			key_words = key_value.split()
			#print(f'Key-words: {key_words}')
			#print(f'Key-value: {key_value}')
			if len(key_words) > 20:
				return await ctx.send("Total number of key-words must be less or equal 20")
			elif len(key_value) < 1:
				return await ctx.send("Total number of key-words must be more than 0")
			else:
				pass
			write_database_data('servers_msg_process', 'key_words', ctx.guild.id, key_value)
			x=[]
			for y in key_value.split():
				x.append('***' + y + '***')
			key_words = " | ".join(x)
			if number <= 0:
				return await ctx.send(f"New key words set as: {key_words}.")
			else:
				if number > 7:
					return await ctx.send(f"Key words set as {key_words}, without limit set. Limit must be less than 7")
				write_database_data('servers_msg_process', 'key_words_limit', ctx.guild.id, number)
				return await ctx.send(f"New key words set as: {key_words}. With apperance limit: {number}")
			
		elif task == 'limit':
			if number == 0:
				return await ctx.send(f"Number can't be 0")
			else:
				if number > 7:
					return await ctx.send(f"Limit must be less than 7")
				write_database_data('servers_msg_process', 'key_words_limit', ctx.guild.id, number)
				return await ctx.send(f"Apperance limit set to: {number}")
			
		elif task == 'penalty':
			penalty = ''
			value = key_value.split()
			if (len(value) != 2):
				return await ctx.send(f"There must be 2 penalties")
			for x in value:
				if x == penalty and not (x == 'pass' or penalty =='pass'):
					return await ctx.send(f"Wrong penalty, there can be 1 penalty for message, and 1 for user")
				if ((x in message_penalties and penalty in message_penalties and not (x == 'pass' or penalty == 'pass')) or (x in user_penalties and penalty in user_penalties and not (x == 'pass' or penalty == 'pass'))):
					return await ctx.send(f"Wrong penalty, there can be 1 penalty for message, and 1 for user")
				if x in message_penalties:
					penalty = penalty + f' {x}' 
				elif x in user_penalties:
					penalty = penalty + f' {x}' 
				else:
					return await ctx.send(f"Unknown penalty {x}")
					#penalty += 'pass'
			if penalty[0] == ' ':
				penalty = penalty[1:]
			write_database_data('servers_msg_process', 'key_words_penalty', ctx.guild.id, penalty)
			return await ctx.send(f"Key words penalty set to: {penalty}")
			
		elif task == 'show':
			key_words=get_database_data('servers_msg_process', 'key_words', ctx.guild.id)
			limit=get_database_data('servers_msg_process', 'key_words_limit', ctx.guild.id)
			check=get_database_data('servers_msg_process', 'key_words_check', ctx.guild.id) or '***No***'
			if key_words:
				x=[]
				for y in key_words.split():
					x.append('***' + y + '***')
				key_words = " | ".join(x)
			else:
				key_words = '***None***'
			if not limit:
				limit = '***None***'
			embed = Embed(title="Detection configuration",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=ctx.me.avatar_url)
			embed.add_field( name='Key words:', value=key_words , inline=True),
			embed.add_field( name=chr(173), value=f"**Key words appaerance limit**: {limit}\n**Key words check**: {check}", inline=False),
			await ctx.send(embed = embed)
			
		else:
			return await ctx.send("Unknown task provided")
	
	@commands.command()
	@commands.has_permissions(administrator=True)
	async def links(self, ctx, task,  *, key_value: typing.Optional[str] = None):
		if task == 'on' or task == 'off':
			if task == 'on':
				value = 'YES'
			else:
				value = 'NO'
			write_database_data('servers_msg_process', 'link_check', ctx.guild.id, value)
			return await ctx.send(f"Links check set to {task}")
		if task == 'penalty':
			penalty = ''
			value = key_value.split()
			if len(value) != 2:
				return await ctx.send(f"There can be max. 2 penalties")
			for x in value:
				if x == penalty and not (x == 'pass' or penalty =='pass'):
					return await ctx.send(f"Wrong penalty, there can be 1 penalty for message, and 1 for user")
				if ((x in message_penalties and penalty in message_penalties and not (x == 'pass' or penalty == 'pass')) or (x in user_penalties and penalty in user_penalties and not (x == 'pass' or penalty == 'pass'))):
					return await ctx.send(f"Wrong penalty, there can be 1 penalty for message, and 1 for user")
				if x in message_penalties:
					penalty = penalty + f' {x}' 
				elif x in user_penalties:
					penalty = penalty + f' {x}' 
				else:
					return await ctx.send(f"Unknown penalty {x}")
					#penalty += 'pass'
			if penalty[0] == ' ':
				penalty = penalty[1:]
			write_database_data('servers_msg_process', 'links_penalty', ctx.guild.id, penalty)
			return await ctx.send(f"Links penalty set to: {penalty}")
		else:
			return await ctx.send("Unknown task")
	
	@commands.command()
	async def msg_process(self, ctx, task, number : typing.Optional[int] = 0,  *, value: typing.Optional[str] = None):
		task = task.lower()
		value = value.lower()
		print(f"Task: {task}\nNumber: {number}\nValue: {value}")
		state = await Processing.msg_process_check(ctx, task, number, value)
		if state:
			pass
		else:
			return 0
		returning_string = await Processing.msg_process_execute(ctx, task, number, value)
		if returning_string:
			return ctx.send(returning_string)
		else:
			pass
	
	@commands.Cog.listener()
	async def on_message(self, message):
		"""
		#await client.process_commands(message)
		if get_database_data('servers_properties', 'message_check_feature', message.guild.id) == 'NO':
			return 0
		
		if get_database_data('servers_msg_process', 'key_words_check', message.guild.id) == 'YES':
			check_links = True
		else:
			check_links = False
		if get_database_data('servers_msg_process', 'link_check', message.guild.id) == 'YES':
			check_key_words = True
		else:
			check_key_words = False
			
		if check_links:
			urls = Processing.check_for_urls(message)
			if urls:
				url_dict = Processing.process_urls(message, urls)
		if check_key_words:
			detected_key_words = Processing.check_for_keys(message, get_database_data('servers_msg_process', 'key_words', message.guild.id))
		
		message_content = ('`' + message.content + '`')
		
		print(f"urls: {urls}\nurl_disct: {url_dict}\nKey_words: {detected_key_words}")
		
		embed = Embed(title="Message flagged",
			      colour = message.author.colour,
			      timestamp=datetime.utcnow()
		)
		embed.set_thumbnail(url=message.author.avatar_url)
		embed.add_field(name= chr(173), value=f"**User**: {message.author} \n**User ID**: {message.author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
		embed.add_field(name="Message content:", value=message_content, inline=False),
		if urls:
			embed.add_field(name='Links flagged:', value= f'There were {len(urls)} links in message.' , inline=False),
		iterate = 0
		for u in url_dict:
			iterate += 1
			embed.add_field(name=f'{iterate} Link:', value= f'{url_dict[url[iterate-1]]}' , inline=False),
		if detected_key_words:
			embed.add_field(name='Key words detected:', value= f'{detected_key_words}' , inline=False),
			#embed.add_field(name=chr(173), value=f"**Key words appaerance limit**: {limit}\n**Key words check**: {check}", inline=False),
		alerts_channel = alert_channel = self.client.get_channel( id = get_database_data('servers_data', 'message_check_channel_id', guild_id) )
		await alerts_channel.send(embed = embed)
								       
		
		return 0 # clear after tests!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	"""
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
	"""
	@commands.Cog.listener()
	async def on_raw_message_delete(self, payload):
		print(f"PAYLOAD: {payload}")
		message = payload.cached_message
		message_channel = self.client.get_channel(payload.channel_id)
		message_guild = self.client.get_guild(payload.guild_id)
		message_channel_id = payload.channel_id
		guild_id = payload.guild_id
		#msg = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
		#author = msg.author
		#print(author.display_name)
		#print("Message deleted")
		modDeleted = False
		database_record = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
		if database_record == None:
			return 0
		deleter = None
		#if (author.bot):
		#	return 0
		if message.content.startswith('$say'):
			return 0
		async for entry in message_guild.audit_logs(limit=1,action=discord.AuditLogAction.message_delete):
			if entry.created_at.now() == datetime.utcnow():
				deleter = entry.user
				#modDeleted = True
		modDeleted = True
		channel = self.client.get_channel( id = database_record )
		embed = discord.Embed( 
			title="Message deleted",
			description="Deleted by moderator" if modDeleted else "Deleted by user",
			color= deleter.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=deleter.icon_url if modDeleted else message.author.avatar_url)
		embed.add_field(name= chr(173), value=f"**Message author**: {author} \n**Message author ID**: {author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Deleter**: {deleter if modDeleted else message.author} \n**Deleter ID**: {deleter.id if modDeleted else author.id}", inline=True),
		embed.add_field(name= chr(173), value=f"**Channel**: {message_channel} \n**Channel ID**: {message_channel_id}", inline=True),
		embed.add_field(name= 'Message content:', value=message.content, inline=True),
		embed.set_footer(text="Provided by Wild West Post Office")
		await channel.send(embed=embed)
	"""
		
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
