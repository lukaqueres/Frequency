import discord, json, io, os, typing, requests, random, asyncio, psycopg2
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

load_dotenv()

intents = discord.Intents().all()
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

tasks = [ 'prefix', 'language', 'channel' ]
values = { 'language' : ( 'english', 'polish', 'angielski', 'polski' ), 'channel' : ( 'updates', 'message_check', 'message_logs' ) }
column = { 'prefix' : 'guild_prefix', 'language' : 'guild_language', 'channel' : { 'message_check' : 'message_check_channel_id', 'updates' : 'updates_channel_id', 'message_logs' : 'logs_msg_channel_id' }}
languages = { ( 'english', 'angielski' ) : 'ENG', ( 'polish', 'polski' ) : 'POL' }

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
		if ( not message.author.guild_permissions.administrator): 
			raise MissingPermissions('You can not use this command')
		if task not in tasks or value = None:
			raise commands.errors.InvalidAttribute
		elif task == 'prefix' and len(value) > 2:
			raise commands.errors.InvalidAttribute('Prefix can be maximum 2 characters long')
		elif value not in values[task] and task != 'prefix':
			raise commands.errors.InvalidAttribute('Invalid value given')
		elif task == 'language' and not languages[value]:
			raise commands.errors.InvalidAttribute('Invalid value given')
		else:
			return 1
		return 0
	
	@staticmethod
	def execute(ctx, task, value, channel):
		guild_id = ctx.guild.id
		channel_id = channel.id or ctx.channel.id
		channel_name = channel.name or ctx.channel.name
		column_name = column[task]
		if task == 'channel':
			column_name = column_name[value]
			await write_database_data('servers_data', column_name, guild_id, channel_id)
			return f'Channel with {value} tag set up succesfully on {channel_name} channel."
		elif task == 'prefix':
			await write_database_data('servers_data', column_name, guild_id, value)
			return f'Prefix set to {value}'
		elif task == 'language':
			language = languages[value]
			await write_database_data('servers_data', column_name, guild_id, languge)
			value = value.capitalize()
			return f"Language set to {value}."
		else:
			return 0
			
class Setup(commands.Cog):
	def __init__(self, client):
		self.client = client
		self.bot = bot
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Setup module loaded')

    
	"""@commands.command()
	@has_permissions(manage_messages=True)
	async def prefix_change(self, ctx, prefix):
		await ctx.send(f'Zmieniono prefix komend na ``{prefix}``')
		print("\n Prefix changed in guild: \" {} \" guild to \"{}\" on \" {} \".".format(ctx.message.guild, prefix, get_time()))
		with open('data.json', 'r') as f:
			prefixes = json.load(f)
      
	prefixes[str(ctx.message.guild.id)] = prefix
    
	with open('data.json','w') as f:
		json.dump(prefixes, f, indent=4)"""
      
	@commands.command()
	async def help(self, ctx):
		message = ctx.message
		embed=discord.Embed(title="Help", description="Pomoc - znajdziesz tu listę oraz informacje dotyczące komend których możesz użyć na tym serwerze", color=0x0000ff)
		embed.add_field(name="$join", value="Dołącza do kanału na którym znajduje się użytkownik.", inline=False)
		embed.add_field(name="$play [ url / słowa kluczowe ]", value="Odtwarza muzykę na kanale głosowym na podstawie adresu url, lub słów kluczowych. Wymaga aby użytkownik znajdował się na kanale głosowym.", inline=False)
		embed.add_field(name="$stop", value="Zatrzymuje odtwarzanie oraz wychodzi z kanału głosowego.", inline=True)
		embed.add_field(name="$volume [ liczba ]", value="Zmienia głośność odtwarzania muzyki na kanale głosowym na określony procent ( domyślnie 50% ).", inline=True)
		if (message.author.guild_permissions.manage_messages):
			embed.add_field(name="Zarządzanie wiadomościami", value="Dostępne jedynie dla użytkowników z uprawnieniem zarządzania wiadomościami.", inline=False)
			embed.add_field(name="$clear [ liczba ]", value="Usuwa określoną liczbę wiadomości z kanału ( nie licząc wiadomości z komendą ).", inline=True)
		if (message.author.guild_permissions.ban_members):
			embed.add_field(name="Zarządzanie użytkownikami", value="Dostępne jedynie dla użytkowników z odpowiednimi uprawnieniami.", inline=False)
			embed.add_field(name="$ban [ użytkownik ]", value="Nakłada bana na użytkownika.", inline=True)
			embed.add_field(name="$unban [ użytkownik ]", value="Usuwa bana z użytkownika, jeżeli go posiada.", inline=True)
		if (message.author.guild_permissions.administrator):
			embed.add_field(name="Zarządzanie serwerem", value="Dostępne jedynie dla użytkowników z uprawnieniami administratora.", inline=False)
			embed.add_field(name="$prefix_change [ prefix]", value="Zmienia prefiks serwera z którego korzysta bot. **UWAGA** działa jedynie przez krótki okres.", inline=False)
		msg = await ctx.send(embed=embed)
		#await msg.add_reaction(':ballot_box_with_check:')
    
#
#<----------> 'set' command - set channels and some settings <------------------------------------------------------------------------>
#

	@commands.command()
	async def set(self, ctx, task, value, channel: typing.Optional[commands.TextChannelConverter] = None):
		if Process.check_tasks(ctx, task, value):
			pass
		else:
			return 0
		returning_string = Process.execute(ctx, task, value, channel)
		if retuning_string:
			return await ctx.say(returning_string)
		else:
			pass
		message = ctx.message
		guild = ctx.guild
		guild_id = guild.id
		channel = ctx.channel
		channel_id = channel.id
		value_length = len(value)
		if (task == 'prefix'): #>-------------------------------------------< Task - prefix
			if (value == 'default'): # If value wasn't changed
				await ctx.send("You must specify new prefix!")
				return 0
			elif (value_length > 2): # If value is too long
				await ctx.send("New prefix length must be long 2 characters max!")
				return 0
			else: # If value seems legit
				cur.execute("UPDATE servers_properties SET guild_prefix = '{}' WHERE guild_id = '{}';".format(value, guild_id))
				con.commit()
				await ctx.send("This guild prefix changed for: '{}'.".format( value ))
		elif (task == 'language'): #>-------------------------------------------< Task - language
			if (value == 'default'): # If value wasn't changed
				await ctx.send("You must specify language!")
				return 0
			elif (value != 'English') and (value != 'Polish') and (value != 'english') and (value != 'polish'): # If value is too long
				await ctx.send("Unknown language, check help command!")
				return 0
			else: # If value seems legit
				if ( value == 'English') or (value == 'english' ): # If value looks like English
					language_name = 'English'
					language = 'ENG'
				elif ( value == 'Polish') or (value == 'polish' ): # If value looks like Polish
					language_name = 'Polish'
					language = 'POL'
				cur.execute("UPDATE servers_properties SET guild_language = '{}' WHERE guild_id = '{}';".format(language, guild_id))
				con.commit()
				await ctx.send("Guild language changed for: '{}'.".format( language_name ))
		elif (task == 'channel'): #>-------------------------------------------< Task - channel set-up
			channel_type = value
			if channel_type == 'message_check': # setting channel type spam info
				if value_two != None:
					channel = value_two
					channel_id = channel.id
				cur.execute("UPDATE servers_data SET message_check_channel_id = '{}' WHERE guild_id = '{}'".format(channel_id, guild_id))
				con.commit()
				await ctx.send("Alerts set up succesfuly on channel: {}!".format( channel ))
			elif channel_type == 'updates': #setting channel type updates about bot
				if value_two != None:
					channel = value_two
					channel_id = channel.id
				cur.execute("UPDATE servers_data SET updates_channel_id = '{}' WHERE guild_id = '{}'".format(channel_id, guild_id))
				con.commit()
				await ctx.send("Information set up succesfuly on channel: {}!".format( channel ))
			elif channel_type == 'message_logs': #setting channel type updates about bot
				if value_two != None:
					channel = value_two
					channel_id = channel.id
				database_data = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
				if channel_id == database_data:
					cur.execute("UPDATE servers_data SET logs_msg_channel_id = {} WHERE guild_id = '{}'".format('NULL', guild_id))
					con.commit()
					return await ctx.send("Message logs cleared up succesfuly on channel: {}!".format( channel ))
				cur.execute("UPDATE servers_data SET logs_msg_channel_id = '{}' WHERE guild_id = '{}'".format(channel_id, guild_id))
				con.commit()
				await ctx.send("Message logs set up succesfuly on channel: {}!".format( channel ))
			else:
				await ctx.send("Unknown channel type, please check if command is properly written or *help* for full guide.")
		else: #>-------------------------------------------------------------< Task - none, inform about it
			await ctx.send("Unknown task, please check if command is properly written or *help* for full guide.")
			return 0
        
    
	@set.error
	async def set_error(self, ctx: commands.Context, error):
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
		elif isinstance(error, commands.errors.ChannelNotFound):
			await ctx.channel.send("Channel not found!")
		else: 
			print(error)
			await ctx.channel.send("There was an error with executing command!")
			
	@commands.command()
	async def toggle(self, ctx, task = None , value = None ):
		if ( not ctx.message.author.guild_permissions.administrator): # If somebody doesn't have permissions to screw with ya'
			await ctx.send("You don't have permissions to do this!")
			return 0
		guild = ctx.guild
		guild_id = guild.id
		if (task == 'Music') or (task == 'music'): #>-------------------------------------------< Task - toggle Music
			database_record = get_database_data('servers_properties', 'music', guild_id)
			if (value == None) and (database_record == 'YES'): # toggle to YES in case of no second argument
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now OFF!")
				if ctx.voice_client != None:
					await ctx.voice_client.disconnect()
					await ctx.send("Bot left voice channel due to Music setting OFF.")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
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
				cur.execute("UPDATE servers_properties SET updates = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Updates setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute("UPDATE servers_properties SET updates = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Updates setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute("UPDATE servers_properties SET updates = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Updates setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute("UPDATE servers_properties SET updates = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
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
				cur.execute("UPDATE servers_properties SET economy = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Economy setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute("UPDATE servers_properties SET economy = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Economy setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute("UPDATE servers_properties SET economy = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Economy setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute("UPDATE servers_properties SET economy = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
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
				cur.execute("UPDATE servers_properties SET message_check_feature = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Message check feature setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'): # toggle to NO in case of no second argument
				cur.execute("UPDATE servers_properties SET message_check_feature = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Message check feature setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'): # toggle to YES
				cur.execute("UPDATE servers_properties SET message_check_feature = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Message check feature setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'): # toggle to NO
				cur.execute("UPDATE servers_properties SET message_check_feature = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
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
	client.add_cog(Setup(client))
