import json, os, discord

# - Import database in case of error -
from packets.database import Database

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
		
	def restrict_Guild(self):
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting status, logging and activities. -
			configuration = json.load(c);
			restrictGuild = configuration["developer"]["restrict-commands"]["to-guild"];
		return discord.Object(id=restrictGuild)

def prefix(client, message):
	with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
		configuration = json.load(c); 
		log = configuration['developer']['log'];
		defaults = configuration['values']['defaults'];
	try:
		database = Database(); # - TODO: Check how to get database object from bot.py main file, for now this will do -
		properties = database.select(table = 'guilds.properties', 
			columns = ['prefix'],
			condition = {"id": message.guild.id}
			);
		prefix = prefix;
	except Exception as e:
		if log['exceptions']:
			prefix = defaults['prefix'];
			print(f'Error while getting prefix: {getattr(e, "message", repr(e))}');
	return prefix;
