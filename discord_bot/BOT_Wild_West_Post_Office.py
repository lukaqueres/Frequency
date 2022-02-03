import discord, json, io, os, typing, requests, random, asyncio, psycopg2, nltk
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot
#from youtube_dl import YoutubeDL
from functions import get_prefix, get_time
load_dotenv()

try:
	DATABASE_URL = os.environ.get('DATABASE_URL')
	con = psycopg2.connect(DATABASE_URL)
	cur = con.cursor()
	print("Bot database opened successfully")
except:
	print("Failed to open database")

intents = discord.Intents.default()
intents.members = True
fetch_offline_members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time

client.remove_command('help')

@client.event #---------------------------------READY---------------------------------------------------------------------------------------------------------
async def on_ready():
	await client.change_presence(status=discord.Status.online, activity=discord.Game('Red Dead Redemption 2'))          #status online/offline  , activity=discord.Game('Red Dead Redemption 2')
	print('Bot logged in with:')
  
async def status_change():
	await client.wait_until_ready()
	statuses = ["Red Dead Redemption 2", "Red Dead Redemption 1", "Red Dead Online", "Red Dead Revolver" ]
	while not client.is_closed():
    		sleep_time = random.randint(1800,3600)
    		status = random.choice(statuses)
    		await client.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
    		print("Activity has been changed to: {}, and next change will be again after: {} seconds." .format(status, sleep_time))
    		await asyncio.sleep(sleep_time)
	client.loop.create_task(status_change())

#----------------------------------------------------------------------------------------COMMANDS-------------------------------------------------------------------------------------------------------------

@client.command()
@has_permissions(manage_messages=True)
async def clear(ctx, number : int ):
	global current_day
	global current_time
	if number > 100:
		return await ctx.send('Sorry, there is a limit of 100 messages.')
	number = number + 1
	print("\n Clear with walue {} has been triggered by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} \".".format(number, ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))
	await ctx.channel.purge(limit = number)

@clear.error
async def clear_error(error, ctx):
	if isinstance(error, MissingPermissions):
		global current_day
		global current_time
		return await ctx.send("Sorry, you can't use that command.")
		print("\n Clear has been triggered and didn't work by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))
		print(" Reason: \" not enough permissions \"")

@client.command() 
#@has_permissions(manage_messages=True)
async def ping(ctx):
	await ctx.send(f'Ping: {round(client.latency * 1000)} ms')
	print("Ping: {} ms on guild: {}" .format(round(client.latency * 1000), ctx.message.guild))
	
@client.command()
@commands.is_owner()
async def say(ctx, *, message):
	await ctx.message.delete()
	if ctx.message.reference:
		message_reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		await ctx.send(message, reference = message_reference)
	await ctx.send(message)
	
@say.error
async def say_error(error, ctx):
	if isinstance(error, MissingPermissions):
		global current_day
		global current_time
		print("\n Say has been triggered and didn't work by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, get_time()))

#>------------------------------------------->INSTALLING ALL THIS USELESS' SHIT<--------------------------------------------------------------------------------------<
	
#>install nltk packages:
packages = { 'averaged_perceptron_tagger', 'wordnet', 'pros_cons', 'reuters', 'hmm_treebank_pos_tagger', 'maxent_treebank_pos_tagger', 'universal_tagset', 'punkt', 'averaged_perceptron_tagger_ru', 'snowball_data', 'rslp', 'porter_test', 'vader_lexicon', 'treebank', 'dependency_treebank', 'stopwords' }
for package in packages:
	nltk.download(package)
	print("{} NLTK package downloaded.".format(package))

#>install all cogs:
for filename in os.listdir('./discord_bot/cogs'):
	if filename.endswith('.py'):
		client.load_extension(f'cogs.{filename[:-3]}')
		
#>just say it's over ( installing of course )
print("All modules, packages installed")
TOKEN = os.environ.get('TOKEN')
client.run(TOKEN)
