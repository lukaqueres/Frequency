# - Importing required unspecified packages -
import json, os, random, asyncio
from random import randrange, randint

# - Importing discord packages -
import discord
from discord.ext import commands, tasks
from discord import Intents, app_commands


# - Importing in-project packages -
from packets.database import Database
from packets.discord import prefix

# - Import cog as a part of slash not-sync work-around -
from cogs.configuration import Configuration

class PIBot(commands.Bot): # discord.Client
	def __init__(self, *, prefix, intents: discord.Intents):
		super().__init__(command_prefix = prefix, intents=intents)
		# A CommandTree is a special type that holds all the application command
		# state required to make it work. This is a separate class because it
		# allows all the extra state to be opt-in.
		# Whenever you want to work with application commands, your tree is used
		# to store and work with them.
		# Note: When using commands.Bot instead of discord.Client, the bot will
		# maintain its own tree instead.
		#self.tree = app_commands.CommandTree(self)
		self.database = Database(); # - Assign database object to client for easy SQL querries -
		self.restrictGuild = self.restrict_Guild();

	# In this basic example, we just synchronize the app commands to one guild.
	# Instead of specifying a guild to every command, we copy over our global commands instead.
	# By doing so, we don't have to wait up to an hour until they are shown to the end-user.
	async def setup_hook(self): # - Guilds restrict is not working for now -
		# This copies the global commands over to your guild.
		self.tree.copy_global_to(guild=self.restrictGuild)
		await self.tree.sync(guild=self.restrictGuild)
		
	async def restrict_Guild(self):
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting status, logging and activities. -
			configuration = json.load(c);
			restrictGuild = configuration["developer"]["restrict-commands"]["to-guild"];
		return discord.Object(id=restrictGuild)

intents = discord.Intents.all() # - Get all Intents TODO: Remember to get messages and other permissions that require discord approval after verification -
# bot = client = commands.Bot(command_prefix = prefix, intents=intents); # - Old client setup, moved to custom class instead -
client = PIBot(prefix = prefix, intents=intents)

#database = Database(); # - Create database object to handle all querries - MOWED TO CUSTOM CLASS ^ INSTEAD -
#client.database = database; # - Assign database object to client for easy fetch from cogs -

# >---------------------------------------< ON application ACTIVE >---------------------------------------< # 
@client.event
async def on_ready():
	with open('configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting status, logging and activities. -
		configuration = json.load(c); 
		status = configuration['discord']['status']; 
		activities = configuration['discord']['activities']; 
		activitiesLists = activities['list-pool'];
		developer = configuration['developer'];
		log = developer['log'];
	statusPool = { "online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle, "dnd": discord.Status.dnd } # - statuses available to be set as bot's status in discord - 
	if developer['active'] and developer["active-status"] in list(statusPool.keys()):
		status = statusPool[developer["active-status"]];
	elif developer['active'] and developer["active-status"] not in list(statusPool.keys()):
		if log['exceptions']:
			print(f"Inappropriate status for developer mode applied: {developer['active-status']} is not a correct status. Try {', '.join(list(statusPool.keys()))}");
		status = statusPool["online"];
	elif status['set'] in statusPool: # - Checking if status given in json file is correct for use, assigning python code if apply, set to online if not. -
		status = statusPool[status['set']];
	elif log['exceptions']:
		print(f"Inappropriate status applied: {status['set']} is not correct status. Try {', '.join(list(statusPool.keys()))}");
		status = statusPool["online"];
	else:
		status = statusPool["online"]; # - End of custom status assign. -
	activity = 'NaN';
	if activities['set']:
		if activities['list'] == 'random': # - Random list means random choice of available lists. -
			alist = activitiesLists[random.choice(activitiesLists.keys())];
		elif activities['list'] in activitiesLists:
			alist = activitiesLists[activities['list']];
		elif log['exceptions']:
			print(f"List of activities not found. Try something other than {activities['list']}");
			alist = False;
		else:
			alist = False;
		activity = random.choice(alist) if alist else None;
		if activities['list'] == 'playing': # - Set special statuses: 'Playing something' or 'Watching something', or just text one. -
			await client.change_presence(status=status, activity=discord.Game(activity));
		elif activities['list'] == 'watching':
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=activity));
		elif activities['list'] == 'listening':
			await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=activity));
		elif activities['list'] == 'none':
			await bot.change_presence(activity=None);
		else:
			await client.change_presence(status=status, activity=discord.Game(activity));
	else:
		await client.change_presence(status=status); # - Change only status if activities are not meant to be set -
		
	if log['notices']:
		listOfGuilds = [];
		for guild in client.guilds:
			listOfGuilds.append(guild.id);
		print(f'----------- APPLICATION ONLINE ----------- \n{len(listOfGuilds)} guilds; status: {status}; activity: {activity}')
		if activity != 'NaN' and activities['cycle']:
			print(f"Activity changing from pool: {activities['list']} in interval: {activities['cycle-interval']}");
	else:
		print('----------- APPLICATION ONLINE -----------')
		
	if activities['cycle'] and activities['set']: # - If set so create looping task to change activity -
		client.loop.create_task(cycleStatus(alist = alist, interval = activities['cycle-interval'], status = status))
	
	# - Sync slash commands tree to global -
	await client.tree.sync()

# - Function to change activity in random time interals -
async def cycleStatus(alist, interval, status):
	await client.wait_until_ready()
	while not client.is_closed():
		if isinstance(interval, int):
			wait = interval;
		elif interval == 'random': # - Interval draw -
			wait = random.randint(900,7200);
		elif interval == 'short':
			wait = random.randint(900,2700);
		elif interval == 'long':
			wait = random.randint(2700,7200);
		else: # - In case of not appropriate interval given ( not short, long, random ). -
			wait = random.randint(1800,3600);
			if log['exceptions']:
				print(f"Interval {interval} not found. \nChanging to random.")
		activity = random.choice(alist);
		await client.change_presence(status=status, activity=discord.Game(name=activity)) # - Changing -
		if log['notices']:
			print(f"New activity: {activity}; next change in {wait} seconds.")
		await asyncio.sleep(wait) # - Wait interval. -

# >---------------------------------------< COMMANDS >---------------------------------------< # 
		
@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Displays ping!"""
    await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}') # interaction.user.mention
	
client.tree.add_command(Configuration(bot), guild=client.restrictGuild) # - Part of slash not-sync work-around -
# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
	configuration = json.load(c); 
	extensions = configuration['extensions'];
	log = configuration['developer']['log'];
if extensions['load']:
	loaded = []; # - Extensions loaded succesfully -
	failed = []; # - Extensions failed to load -
	for cog in os.listdir(extensions['directory']):
		if cog.endswith('.py'):	 # - Every file from directory path with .py extension is threated as cog. -
			if not cog[:-3] in extensions['ignore']:
				try:
					client.load_extension(f"{extensions['directory']}.{cog[:-3]}");
					loaded.append(cog[:-3]);
				except Exception as e: # - Catch exception in loading, can be extended. -
					failed.append([cog[:-3], getattr(e, 'message', repr(e))]);
			else:
				failed.apped([cog[:-3], 'Extension ignored.']);
	if log['notices'] and len(loaded) != 0:
		print(f"Extensions loaded ({len(loaded)}): {', '.join(str(l) for l in loaded)}" ); # - Log loaded cogs with it's number and list. -
	if log['exceptions'] and len(failed) != 0:
		print(f"Failed to load ({len(failed)}) extensions: {', '.join(str(f[0] + ': ' + f[1]) for f in failed)}"); # - Log failed cogs with it's number and list. -

# - TODO: Check if it will actually sync global commands -
#guild = guild;#ctx.guild # or discord.Object(id=...)  # you can use a full discord.Guild as the method accepts a Snowflake
#Bot.tree.copy_global_to(guild=guild)

TOKEN = os.environ.get('TOKEN')

if __name__ == "__main__":
	client.run(TOKEN)
		
