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
	async def set(self, ctx, task = 'default', value = 'default', value_two: commands.TextChannelConverter = None):
		message = ctx.message
		guild = ctx.guild
		guild_id = guild.id
		channel = ctx.channel
		channel_id = channel.id
		value_length = len(value)
		if (task == 'prefix'): #>-------------------------------------------< Task - prefix
			if ( not message.author.guild_permissions.administrator): # If somebody doesn't have permissions to screw with ya'
				await ctx.send("You don't have permissions to do this!")
				return 0
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
			if ( not message.author.guild_permissions.administrator): # If somebody doesn't have permissions to screw with ya'
				await ctx.send("You don't have permissions to do this!")
				return 0
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
			if ( not ctx.message.author.guild_permissions.administrator): # If somebody doesn't have permissions to screw with ya'
				await ctx.send("You don't have permissions to do this!")
				return 0
			channel_type = value
			if channel_type == 'spam_info': # setting channel type spam info
				if value_two != None:
					channel = value_two
					channel_id = channel.id
				cur.execute("UPDATE servers_data SET anty_spam_channel_id = '{}' WHERE guild_id = '{}'".format(channel_id, guild_id))
				con.commit()
				await ctx.send("Information set up succesfuly on channel: {}!".format( channel ))
			elif channel_type == 'updates': #setting channel type updates about bot
				if value_two != None:
					channel = value_two
					channel_id = channel.id
				cur.execute("UPDATE servers_data SET updates_channel_id = '{}' WHERE guild_id = '{}'".format(channel_id, guild_id))
				con.commit()
				await ctx.send("Information set up succesfuly on channel: {}!".format( channel ))
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
			await ctx.channel.send("There was an error with executing command!")
			
	@commands.command()
	async def toggle(self, ctx, task = None , value = None ):
		guild = ctx.guild
		guild_id = guild.id
		if (task == 'Music') or (task == 'music'):
			database_record = get_database_data('servers_properties', 'music', guild_id)
			if (value == None) and (database_record == 'YES'):
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now OFF!")
				return 0
			elif (value == None) and (database_record == 'NO'):
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'ON') and (database_record == 'NO'):
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('YES', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now ON!")
				return 0
			elif (value == 'OFF') and (database_record == 'YES'):
				cur.execute("UPDATE servers_properties SET music = '{}' WHERE guild_id = '{}'".format('NO', guild_id))
				con.commit()
				await ctx.channel.send("Music setting is now OFF!")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'):
				await ctx.channel.send("Music setting is already OFF!")
				return 0
			elif (value == 'OFF') and (database_record == 'NO'):
				await ctx.channel.send("Music setting is already OFF!")
				return 0
			else:
				await ctx.channel.send("There was an error while changing music setting state!")
				return 0
def setup(client):
	client.add_cog(Setup(client))
