import json, os, discord

from typing import Optional
from discord.ext import commands, tasks
# - Import database in case of error -
from packets.database import Database
from packets.time import Time
"""

TIPS IN TOPIC OF EMBEDS:

1. Use `chr(173)` as an ampty field, f. ex. `name=chr(173)`;

2. Syntax `"Made by [lukaqueres](https://github.com/lukaqueres)"` will display text 'lukaqueres' as a hyperlink leading to url ( in this case to: https://github.com/lukaqueres );

"""

class PIEmbed(discord.Embed): # - Create custom PIEmbed ( Plan It Embed ) embed to pre-set attributes and add functions -
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.time = Time();
		self.add = AddEmbedFields(self)
		self.timestamp = self.time.UTCNow() # - Assign timestamp !NOTE: Timestamp will show embed object construct time; Use function `revokeTimestamp` to re-set -
		text = self.__footerText();
		self.set_footer(text=text) # - Create custom footer as it will be pretty much the same for all (PI)Embeds -
		self.color = discord.Color.blurple() # - Assign color `blurple` as an (PI)Embed color. Pretty nice I think  -
		
	def __footerText(self): # - Create footer text from app name from JSON -
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file and fetch app name. -
			configuration = json.load(c); 
			appName = configuration['name'];
		text = f'Provided by {appName}'; # - Make nice text, so apart from nick name, everything will SCREAM `PLAN IT`, `PLAN IT`... khem, just make footer text, can be changed -
		return text;
	
	def revokeTimestamp(self): # - Simple function to re-setting timestamp, use in case of long time span between `construct -> send` -
		self.timestamp = self.time.UTCNow()
		
	def lenCheck(self): # - As embeds have 6000 caracters limit, it is important to keep them below that value. Will be expanded in future -
		if len(self) > 6000:
			return False;
		else:
			return True;
		
class AddEmbedFields(PIEmbed):
	def __init__(self, embed):
		self.embed = embed;
		self.content_limit = 1024 # - content/value limit is exacly 1024 caracters, when more, error will be raised -
		self.title_limit = 256 # - title/name limit is 256 caracters, when more, error will trigger -
		self.empty_value = "chr(173)" # - empty value, will show box in embed as empty, without rasing any exceptions -
		self.default_inline = False # - default value for if field should be inline or not -
		
	def field(self, index: Optional[int] = None, title: Optional[str] = None, content: Optional[str] = None, inline: Optional[bool] = False):
		print(f'title: {len(title)}, content: {len(content)}')
		if len(title) > self.title_limit:
			title = title[0:self.title_limit];
		if len(content) > self.content_limit:
			dividings = [];
			dividepoints = []
			for i in range((self.content_limit // len(content)) + 1):
				if len(dividepoints) == 0:
					dividepoints.push(len(content) / ((self.content_limit // len(content)) + 1));
				else:
					dividepoints.push(dividepoints * len(dividepoints))
			print(f'dividepoints: {dividepoints}')
		self.embed.add_field(name="TEST", value="*PASSED*", inline=False);
		
	def emptyField(self, index: Optional[int] = None):
		if index >= 0:
			self.embed.insert_field_at(index=index, name=self.empty_value, value=self.empty_value, inline=self.default_inline)
		else:
			self.embed.add_field(name=self.empty_value, value=self.empty_value, inline=self.default_inline);
		
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
		self.time = Time();
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
