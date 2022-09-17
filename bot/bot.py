# - Importing required unspecified packages -
import json, os, random, asyncio, traceback, sys
from random import randrange, randint

# - Importing discord packages -
import discord
from discord.ext import commands, tasks
from discord import Intents, app_commands


# - Importing in-project packages -
from packets.database import Database
from packets.discord import PIBot

# - Import cog as a part of slash not-sync work-around -
#from cogs.configuration import ConfigurationGroup


intents = discord.Intents.all() # - Get all Intents TODO: Remember to get messages and other permissions that require discord approval after verification -
# bot = client = commands.Bot(command_prefix = prefix, intents=intents); # - Old client setup, moved to custom class instead -
client = PIBot()

#database = Database(); # - Create database object to handle all querries - MOWED TO CUSTOM CLASS ^ INSTEAD -
#client.database = database; # - Assign database object to client for easy fetch from cogs -

asyncio.run(startup());

# >---------------------------------------< ON application ACTIVE >---------------------------------------< # 
@client.event
async def on_ready():
	with open('configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting status, logging and activities. -
		configuration = json.load(c); 
		status = configuration['discord']['status']; 
	statuses = { "online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle, "dnd": discord.Status.dnd } # - statuses available to be set as bot's status in discord - 
	activitiesList = { "watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening} # - Available activities types, `playing` not included due to diffrent setup procedure -
	if self.configuration.read(category="overview", key="developer.active"):
		status = self.configuration.read(category="overview", key="developer.discord-status")
		if status not in list(statuses.keys()):
			raise ValueError("`{}` status is not supported, try instead: {}".format(status, ', '.join(list(statusPool.keys()))));	
		status = statuses[status]
	elif self.configuration.read(category="overview", key="discord.status.set") not in list(statuses.keys()): # - Checking if status given in json file is correct for use, assigning python code if apply, set to online if not. -
		raise ValueError("`{}` status is not supported, try instead: {}".format(status, ', '.join(list(statusPool.keys()))));
	else:	 
		status = statuses[self.configuration.read(category="overview", key="discord.status.set")];
		# - End of custom status assign. -
		
	# - Assingning custom activity status to bot -
	if self.configuration.read(category="overview", key="discord.activity.set"):
		activities = self.configuration.read(category="overview", key="discord.activity.list");
		pool = self.configuration.read(category="overview", key="discord.activity.pool");
		if self.configuration.read(category="overview", key="developer.active"):
			activities = self.configuration.read(category="overview", key="developer.discord-custom-sctivity");
		elif activities == 'random': # - Random list means random choice of available lists. -
			activities = pool[random.choice(list(pool.keys()))];
		elif activities in list(pool.keys()):
			activities = pool[activities];
		else:
			raise ValueError("`{}` activities list not found".format(activities));
		if len(activities['list']) == 0:
			raise ValueError("List of custom statuses can not be empty, set activity to false in such case");	 
		activity = random.choice(activities['list'])
		if activities['type'] == 'playing': # - Set special statuses: 'Playing something' or 'Watching something' etc. -
			await client.change_presence(status=status, activity=discord.Game(activity));
		elif activities['type'] in list(activitiesList.keys()):
			await bot.change_presence(activity=discord.Activity(type=activitiesList[activities['type']], name=activity));
		else:
			raise ValueError("{} is not a valid activity type".format(activities['type']));
	else:
		await client.change_presence(status=status); # - Change only status if activities are not meant to be set -
	
	clientGuildsIds = [];
	for guild in client.guilds:
		clientGuildsIds.append(guild.id);
	client.log.hard('- - - - - - - - - - - APPLICATION ONLINE - - - - - - - - - - -')
	client.log.notify('{} guilds; status: {}; activity: {}'.format(len(clientGuildsIds), status, activity or 'None'))
	if self.configuration.read(category="overview", key="discord.activity.set") and self.configuration.read(category="overview", key="discord.activity.cycle"):
		client.log.notify("Activity changing from pool: {} in interval: {}".format(', '.join(activities['list']), self.configuration.read(category="overview", key="discord.activity.cycle-interval")));
		client.loop.create_task(cycleStatus(activities = activities, interval = self.configuration.read(category="overview", key="discord.activity.cycle-interval"), status = status))
	
	# - Sync slash commands tree to global -
	await client.tree.sync()

#@on_ready.error
#async def on_ready_error(error):
#	print('Error ' + str(type(error)) + ', '.join(list(inst.args)))
#	traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	
# - Function to change activity in random time interals -
async def cycleStatus(activities, interval, status):
	activitiesList = { "watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening} # - Available activities types, `playing` not included due to diffrent setup procedure -
	await client.wait_until_ready()
	while not client.is_closed():
		if isinstance(interval, int):
			time = interval;
		elif interval == 'random': # - Interval draw -
			time = random.randint(900,7200);
		elif interval == 'short':
			time = random.randint(900,2700);
		elif interval == 'long':
			time = random.randint(2700,7200);
		else: # - In case of not appropriate interval given ( not: short, long, random ). -
			raise ValueError("{} is not a valid interval".format(interval));
		activity = random.choice(activities[list]);
		if activities['type'] == 'playing': # - Set special statuses: 'Playing something' or 'Watching something' etc. -
			await client.change_presence(status=status, activity=discord.Game(activity));
		elif activities['type'] in list(activitiesList.keys()):
			await bot.change_presence(activity=discord.Activity(type=activitiesList[activities['type']], name=activity));
		if log['notices']:
			client.log.notify("Changed activity: {}; Waiting {} seconds.".format(activity, time))
		await asyncio.sleep(time) # - Wait interval. -

# >---------------------------------------< COMMANDS >---------------------------------------< # 
		
@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Displays ping!"""
    await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}', ephemeral = True) # interaction.user.mention
	
#client.tree.add_command(ConfigurationGroup(client)) #, guild=client.restrictGuild - Part of slash not-sync work-around -
# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
async def startup():
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
						await client.load_extension(f"{extensions['directory']}.{cog[:-3]}");
						loaded.append(cog[:-3]);
					except Exception as e: # - Catch exception in loading, can be extended. -
						failed.append([cog[:-3], getattr(e, 'message', repr(e))]);
				else:
					failed.apped([cog[:-3], 'Extension ignored.']);
		if len(loaded) != 0:
			client.log.notify(f"Extensions loaded ({len(loaded)}): {', '.join(str(l) for l in loaded)}"); # - Log loaded cogs with it's number and list. -
		if log['exceptions'] and len(failed) != 0:
			client.log.notify(f"Failed to load ({len(failed)}) extensions: {', '.join(str(f[0] + ': ' + f[1]) for f in failed)}"); # - Log failed cogs with it's number and list. -
		
		async with client:
			TOKEN = os.environ.get('TOKEN')
			await client.start(TOKEN)

#if __name__ == "__main__":
#	client.run(TOKEN)
		
