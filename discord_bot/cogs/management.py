import discord, json, io, os, typing, requests, random, asyncio, psycopg2
from os import getenv
import sys
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot

from functions import get_prefix, get_time, get_database_data, write_database_data

load_dotenv()

intents = discord.Intents().all()
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

tasks = [ 'prefix', 'language', 'channel' ]
values = { 'language' : [ 'english', 'polish', 'angielski', 'polski' ], 'channel' : [ 'updates', 'message_check', 'message_logs' ] }
column = { 'prefix' : 'guild_prefix', 'language' : 'guild_language', 'channel' : { 'message_check' : 'message_check_channel_id', 'updates' : 'updates_channel_id', 'message_logs' : 'logs_msg_channel_id' }}
languages = { 'english' : 'ENG', 'polish' : 'POL' }

                 # This dictionary is used to store toggle tasks, and easly add new if needed
toggleables = {  # 'KEY-WORD used' : 'proper column name in database' OR ( proper column name in database, Required channel id set to activate )
	'music' : 'music',
	'updates' : [ 'updates', 'updates_channel_id' ],
	'message_check' : [ 'message_check_feature', 'message_check_channel_id' ],
	'economy' : 'economy'
	 }

settings = { 'off' : 'NO', 'on' : 'YES', 'YES' : 'ON', 'NO' : 'OFF' } # This dictionary is only for saving YES/NO type information in to database, and converting it to/from nice 'ON' and 'OFF'

class Process:
	def __init__(self, task, value_one, value_two, channel : typing.Optional[commands.TextChannelConverter]):
		self.client = client
		self._author = ctx.message.author
		self._authorPerimissions = message.author.guild_permissions
		self._task = task
		self._value = value_one
		self._valueTwo = valu_two
		self._channel = channel
			
	@staticmethod
	def check_tasks(ctx, task, value):
		if ( not ctx.message.author.guild_permissions.administrator ): # Whell, it checks if caller has required permissions ( for setup commands it is ALWAYS administrator )
			raise MissingPermissions('You can not use this command')
		
		if task in toggleables.keys():                                                                           # It means toggle command was called WITH propper task name
			if settings[value] == get_database_data('servers_properties', toggleables[task][0] if isinstance(toggleables[task], list) else toggleables[task], ctx.guild.id):      # In case value is the same
				raise commands.BadArgument(f'{task.capitalize()} is already set to {settings[value]}')
			if  not isinstance(toggleables[task], list):                                                   # If it don't need any other setting ( channel )
				return 1
			elif isinstance(toggleables[task], list):                                                      # If it is list, so it require setting ( channel )
				if  get_database_data('servers_data', toggleables[task][1], ctx.guild.id):       # Check if required setting ( channel ) is set
					return 1
				else:                                                                                  # When required setting ( channel ) is not set
					raise commands.BadArgument(f'{task.capitalize()} require special channel to be set before.')
			else:                                                                                          # I don't really have any idea when it is called
				raise commands.BadArgument(f'There was error with checking {task} requirements.')
			                                                      # \/ update it to be more flexible \/ 'n used with set command
		if task == 'prefix' and len(value) <= 2:
			return 1
		if task not in tasks or value == None:
			raise commands.MissingRequiredArgument('Required attribute missing')
		elif task == 'prefix' and len(value) > 2:
			raise commands.BadArgument('Prefix can be maximum 2 characters long')
		elif value not in values[task] and task != 'prefix':
			raise commands.BadArgument('Invalid value given')
		elif task == 'language' and not languages[value]:
			raise commands.BadArgument('Invalid value given')
		else:
			return 1
		return 0
	
	@staticmethod
	def execute(ctx, task, value, channel = None):
		
		if task in toggleables.keys():        #again we are working on tasks from toggle command and as everything was checked in check_tasks ( I hope so ) we just execute it
			set_value = settings[value]
			column = toggleables[task][0] if isinstance(toggleables[task], list) else toggleables[task] # column in db to save in to : set to index 0 in list, or simply translate if not list
			write_database_data('servers_properties', column, ctx.guild.id, set_value)
			return f'Success! {task.capitalize()} has been set to {value.upper()}'
			
		guild_id = ctx.guild.id
		channel = channel or ctx.channel
		channel_id = channel.id or ctx.channel.id
		channel_name = channel.name or ctx.channel.name
		column_name = column[task]
		if task == 'channel':
			column_name = column_name[value]
			write_database_data('servers_data', column_name, guild_id, channel_id)
			return f'Channel with {value} tag set up succesfully on {channel_name} channel.'
		elif task == 'prefix':
			write_database_data('servers_properties', column_name, guild_id, value)
			return f'Prefix set to {value}'
		elif task == 'language':
			language = languages[value]
			write_database_data('servers_properties', column_name, guild_id, language)
			value = value.capitalize()
			return f"Language set to {value}."
		else:
			return 0
			
class Management(commands.Cog):
	"""Commands for setting up, and configuring bot"""
	def __init__(self, client):
		self.client = client
		self.bot = bot
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Management module loaded')

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
#
#<----------> 'set' command - set channels and some settings <------------------------------------------------------------------------>
#

	@commands.command()
	async def set(self, ctx, task, value, channel: typing.Optional[commands.TextChannelConverter] = None):
		task = task.lower()
		value = value.lower()
		if Process.check_tasks(ctx, task, value):
			pass
		else:
			return 0
		returning_string = Process.execute(ctx, task, value, channel)
		if returning_string:
			return await ctx.send(returning_string)
		else:
			pass
			
	@commands.command()
	async def toggle(self, ctx, task, value = None ):
		task = task.lower()
		if value == None:
			dbvalue = get_database_data('servers_properties', toggleables[task][0] if isinstance(toggleables[task], list) else toggleables[task], ctx.guild.id)
			if dbvalue == 'YES':
				value = 'off'
			else: 
				value = 'on'
		else:
			value = value.lower()
		if Process.check_tasks(ctx, task, value):
			pass
		else:
			return 0
		returning_string = Process.execute(ctx, task, value)
		if returning_string:
			return await ctx.send(returning_string)
		else:
			pass
		
		guild = ctx.guild
		guild_id = guild.id
		if (task == 'Music') or (task == 'music'): #>-------------------------------------------< Task - toggle Music
			database_record = get_database_data('servers_properties', 'music', guild_id)
			if (value == None) and (database_record == 'YES'): # toggle to YES in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET music = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Music setting is now OFF!")
				if ctx.voice_client != None:
					await ctx.voice_client.disconnect()
					await ctx.send("Bot left voice channel due to Music setting OFF.")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET music = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute(
					"UPDATE servers_properties SET music = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute(
					"UPDATE servers_properties SET music = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Music setting is now OFF!")
				if ctx.voice_client != None:
					await ctx.voice_client.disconnect()
					await ctx.send("Bot left voice channel due to Music setting OFF.")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Music setting is already OFF!")
				return 0
			elif (value == 'ON') and (database_record == 'YES'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Music setting is already ON!")
				return 0
			else: # Just to have some nice error information ( It's like base, yes? ) and have hope to never show that message.
				await ctx.channel.send("There was an error while changing music setting state!")
				return 0
		elif (task == 'Updates') or (task == 'updates') or (task == 'Update') or (task == 'update'): #>-------------------------------------------< Task - toggle Updates
			database_record = get_database_data('servers_properties', 'updates', guild_id)
			database_record_two = get_database_data('servers_data', 'updates_channel_id', guild_id)
			if ((database_record_two == None) and (value == 'YES')) or ((database_record_two == None) and (database_record == 'NO')):
				return await ctx.channel.send("Can't turn ON while there is none channel set for alerts!")
			if (value == None) and (database_record == 'YES'): # toggle to YES in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET updates = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Updates setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET updates = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Updates setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute(
					"UPDATE servers_properties SET updates = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Updates setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute(
					"UPDATE servers_properties SET updates = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Updates setting is now OFF!")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Updates setting is already OFF!")
				return 0
			elif (value == 'ON') and (database_record == 'YES'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Updates setting is already ON!")
				return 0
			else: # Just to have some nice error information ( It's like base, yes? ) and have hope to never show that message.
				await ctx.channel.send("There was an error while changing updates setting state!")
				return 0
		elif (task == 'Economy') or (task == 'economy'): #>-------------------------------------------< Task - toggle Economy
			database_record = get_database_data('servers_properties', 'economy', guild_id)
			if (value == None) and (database_record == 'YES'): # toggle to YES in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET economy = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Economy setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET economy = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Economy setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute(
					"UPDATE servers_properties SET economy = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Economy setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute(
					"UPDATE servers_properties SET economy = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Economy setting is now OFF!")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Economy setting is already OFF!")
				return 0
			elif (value == 'ON') and (database_record == 'YES'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Economy setting is already ON!")
				return 0
			else: # Just to have some nice error information ( It's like base, yes? ) and have hope to never show that message.
				await ctx.channel.send("There was an error while changing updates setting state!")
				return 0
		elif (task == 'Message_check') or (task == 'message_check'): #>-------------------------------------------< Task - toggle Spam check
			database_record = get_database_data('servers_properties', 'message_check_feature', guild_id)
			database_record_two = get_database_data('servers_data', 'message_check_channel_id', guild_id)
			if ((database_record_two == None) and (value == 'YES')) or ((database_record_two == None) and (database_record == 'NO')):
				return await ctx.channel.send("Can't turn ON while there is none channel set for alerts!")
			if (value == None) and (database_record == 'YES'): # toggle to YES in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET message_check_feature = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Message check feature setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute(
					"UPDATE servers_properties SET message_check_feature = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Message check feature setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute(
					"UPDATE servers_properties SET message_check_feature = %s WHERE guild_id = %s",
					('YES', guild_id)
				)
				con.commit()
				await ctx.channel.send("Message check feature setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute(
					"UPDATE servers_properties SET message_check_feature = %s WHERE guild_id = %s",
					('NO', guild_id)
				)
				con.commit()
				await ctx.channel.send("Message check feature setting is now OFF!")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Message check feature setting is already OFF!")
				return 0
			elif (value == 'ON') and (database_record == 'YES'): # If user request is already active setting tell him so n' do nothin'
				await ctx.channel.send("Message check feature setting is already ON!")
				return 0
			else: # Just to have some nice error information ( It's like base, yes? ) and have hope to never show that message.
				await ctx.channel.send("There was an error while changing message check setting state!")
				return 0
		else:
			await ctx.channel.send("You must choose what to change!")
			
def setup(client):
	client.add_cog(Management(client))
