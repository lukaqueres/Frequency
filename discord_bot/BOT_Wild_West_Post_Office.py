import discord, json, io, os, typing, requests, random, asyncio, psycopg2, nltk
from os import getenv
import contextlib, datetime
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


class HelpEmbed(discord.Embed): # Our embed with some preset attributes to avoid setting it multiple times
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.timestamp = datetime.utcnow()
		text = "Use help [command] or help [category] for more information | <> is required | [] is optional"
		self.set_footer(text=text)
		self.color = discord.Color.blurple()


class MyHelp(commands.HelpCommand):
	def __init__(self):
		super().__init__( # create our class with some aliases and cooldown
			command_attrs={
				"help": "The help command for the bot",
				"cooldown": commands.Cooldown(1, 3.0, commands.BucketType.user),
				"aliases": ['commands']
			}
		)
    
	async def send(self, **kwargs):
		"""a short cut to sending to get_destination"""
		await self.get_destination().send(**kwargs)

	async def send_bot_help(self, mapping):
		"""triggers when a `<prefix>help` is called"""
		ctx = self.context
		embed = HelpEmbed(title=f"{ctx.me.display_name} Help")
		embed.set_thumbnail(url=ctx.me.avatar_url)
		usable = 0 

		for cog, commands in mapping.items(): #iterating through our mapping of cog: commands
			if filtered_commands := await self.filter_commands(commands): 
				# if no commands are usable in this category, we don't want to display it
				amount_commands = len(filtered_commands)
				usable += amount_commands
				if cog: # getting attributes dependent on if a cog exists or not
					name = cog.qualified_name
					description = cog.description or "No description"
				else:
					name = "Other"
					description = "Commands with no category"

				embed.add_field(name=f"{name} Category [{amount_commands}]", value=description)

		embed.description = f"{len(bot.commands)} commands | {usable} usable" 

		await self.send(embed=embed)

	async def send_command_help(self, command):
		"""triggers when a `<prefix>help <command>` is called"""
		#signature = self.get_command_signature(command) # get_command_signature gets the signature of a command in <required> [optional]
		prefix = get_command_signature(command)[0]
		signature = ( str(prefix) + command.usage )
		embed = HelpEmbed(title=signature, description=f'Also can be used as ( aliaces ): {command.aliases}' if command.aliases else "No aliases available for this command.") #help
		embed.add_field(name="Description", value=command.description or "No description found...", inline=False)
		if cog := command.cog:
			embed.add_field(name="Category", value=cog.qualified_name)

		can_run = "No"
		# command.can_run to test if the cog is usable
		with contextlib.suppress(commands.CommandError):
			if await command.can_run(self.context):
				can_run = "Yes"
            
		embed.add_field(name="Usable", value=can_run)

		if command._buckets and (cooldown := command._buckets._cooldown): # use of internals to get the cooldown of the command
			embed.add_field(
				name="Cooldown",
				value=f"{cooldown.rate} per {cooldown.per:.0f} seconds",
			)

		await self.send(embed=embed)

	async def send_help_embed(self, title, description, commands): # a helper function to add commands to an embed
		embed = HelpEmbed(title=title, description=description or "No description found...")

		if filtered_commands := await self.filter_commands(commands):
			for command in filtered_commands:
				embed.add_field(name=command.usage or self.get_command_signature(command), value=command.brief or "No command brief found") # brief = help
           
		await self.send(embed=embed)

	async def send_group_help(self, group):
		"""triggers when a `<prefix>help <group>` is called"""
		title = self.get_command_signature(group)
		await self.send_help_embed(title, group.help, group.commands)

	async def send_cog_help(self, cog):
		"""triggers when a `<prefix>help <cog>` is called"""
		title = cog.qualified_name or "No"
		await self.send_help_embed(f'{title} Category', cog.description, cog.get_commands())
        

bot.help_command = MyHelp()

client = commands.Bot(command_prefix = get_prefix, intents=intents, help_command=MyHelp())
bot = client

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time

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
	
@client.command(hidden = True)
@commands.is_owner()
async def say(ctx, *, message):
	await ctx.message.delete()
	if ctx.message.reference:
		message_reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
		return await ctx.send(message, reference = message_reference)
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
