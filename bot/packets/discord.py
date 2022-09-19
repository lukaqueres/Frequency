import json, os, random, asyncio, traceback, sys

import discord

from typing import Optional
from discord.ext import commands, tasks
# - Import database in case of error -
from packets.database import Database
from packets.time import Time
from packets.utilities import Configuration, Logger
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
		#self.set_author(name=self.__appName())
		self.color = discord.Color.blurple() # - Assign color `blurple` as an (PI)Embed color. Pretty nice I think  -
		self.set_thumbnail(url=None);
		
	def __footerText(self): # - Create footer text from app name from JSON -
		text = f'Provided by {self.__appName()}'; # - Make nice text, so apart from nick name, everything will SCREAM `PLAN IT`, `PLAN IT`... khem, just make footer text, can be changed -
		return text;
	
	def __appName(self):
		appName = self.database.client.configuration.read(category="utilities", key="name")
		return appName			
	
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
		self.embed_limit = 6000 # - There is a limit of 6000 caracters in one embed -
		self.title_limit = 256 # - title/name limit is 256 caracters, when more, error will trigger. Title applies for Embed title -
		self.description_limit = 4096 # - Embed description can be 4096 caracters long. Can be used for short info without names whitespaces - 
		self.name_limit = 256 # - name applies for field names, they can be 256 caracters long each -
		self.field_limit = 25 # - There can be only 25 fields per embed -
		self.value_limit = 1024 # - content/value limit is exacly 1024 caracters, when more, error will be raised, applu for fields value ( content ) -
		self.footer_limit = 2048
		self.empty_value = "\u200b" #'chr(173)' # - empty value, will show box in embed as empty, without rasing any exceptions -
		self.default_inline = False # - default value for if field should be inline or not -
		
	def __divideString(self, string, index):
		if index >= len(string):
			return string, None;
		elif index <= 0:
			return None, string;
		else:
			return string[:index], string[index:]
		
	def field(self, index: Optional[int] = None, name: Optional[str] = None, value: Optional[str] = None, inline: Optional[bool] = False) -> None:
		if len(self.embed.fields) == self.field_limit:
			return False # - Return False if fileld limit reached TODO: Raise exception `fields limit reached` -
		if not name and not value:
			self.emptyField(index);
		#print(f'title: {len(name)}, content: {len(value)}')
		if len(name) > self.name_limit:
			name = name[0:self.title_limit]; # - Cut field name to fit limit. TODO: Add error for such cases -
		values = [];
		if len(value) > self.value_limit:
			print(f'timesx: {(len(value) // self.value_limit) + 1}');
			for x in range((len(value) // self.value_limit) + 1):
				divide = len(value) // ((len(value) // self.value_limit) + 1)
				print(f'divide in: {divide}');
				divideInSpace = value.rindex(' ', 0, divide);
				if ((divide-divideInSpace) < 10):
					divide = divideInSpace
				cut, value = self.__divideString(value, divide);
				values.append(cut);
		else:
			values.append(value);
		if len(values) > 1:
			inline = False;
		for value in values:
			if values.index(value) != 0:
				name = self.empty_value;
			if len(self.embed.fields) == self.field_limit:
				return False # - Return False if fileld limit reached TODO: Raise exception `fields limit reached` -
			if not index:
				self.embed.add_field(name=name, value=value, inline=inline);	
			else:
				self.embed.insert_field_at(index=index, name=name, value=value, inline=inline)
				index += 1
		
	def emptyField(self, index: Optional[int] = None, inline: Optional[bool] = False):
		if len(self.embed.fields) == self.field_limit:
			return False # - Return False if fileld limit reached TODO: Raise exception `fields limit reached` -
		if index >= 0:
			self.embed.insert_field_at(index=index, name=self.empty_value, value=self.empty_value, inline=inline or self.default_inline)
		else:
			self.embed.add_field(name=self.empty_value, value=self.empty_value, inline=self.default_inline);
			
class PIBot(commands.Bot): # discord.Client
	def __init__(self, **kwargs):
		super().__init__(command_prefix = self.__get_prefix, intents=discord.Intents.all())
		# A CommandTree is a special type that holds all the application command
		# state required to make it work. This is a separate class because it
		# allows all the extra state to be opt-in.
		# Whenever you want to work with application commands, your tree is used
		# to store and work with them.
		# Note: When using commands.Bot instead of discord.Client, the bot will
		# maintain its own tree instead.
		#self.tree = app_commands.CommandTree(self)
		self.database = Database(self); # - Assign database object to client for easy SQL querries -
		self.time = Time();
		self.configuration = Configuration();
		self.log = Logger(self, "logs.txt");
		self.restrictGuild = self.__restrict_Guild();

	# In this basic example, we just synchronize the app commands to one guild.
	# Instead of specifying a guild to every command, we copy over our global commands instead.
	# By doing so, we don't have to wait up to an hour until they are shown to the end-user.
	async def setup_hook(self): # - Guilds restrict is not working for now -
		# This copies the global commands over to your guild.
		#self.tree.copy_global_to(guild=self.restrictGuild)
		#await self.tree.sync(guild=self.restrictGuild)
		self.tree.copy_global_to(guild=self.restrictGuild)
		await self.tree.sync()
		
	def __restrict_Guild(self):
		guildId = self.configuration.read(category="utilities", key="developer.commands.restrict_to")
		return discord.Object(id=guildId)
	
	def __get_prefix(self, client, message: discord.Message):
		try:
			prefix = self.database.select(table = 'guilds.properties', 
				columns = ['prefix'],
				condition = {"id": message.guild.id}
				);
			prefix = prefix;
		except Exception as e:
			prefix = self.configuration.read(category="utilities", key="database.defaults.prefix");
			self.log.exception(f'Error while getting prefix: {getattr(e, "message", repr(e))}');
		return prefix;
		
	async def on_ready(self):
		try:
			statuses = { "online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle, "dnd": discord.Status.dnd } # - statuses available to be set as bot's status in discord - 
			activitiesList = { "watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening} # - Available activities types, `playing` not included due to diffrent setup procedure -
			if self.configuration.read(category="overview", key="developer.active"):
				status = self.configuration.read(category="overview", key="developer.discord-status")
				if status not in list(statuses.keys()):
					raise ValueError("`{}` status is not supported, try instead: {}".format(status, ', '.join(list(statuses.keys()))));	
				status = statuses[status]
			elif self.configuration.read(category="overview", key="discord.status.set") not in list(statuses.keys()): # - Checking if status given in json file is correct for use, assigning python code if apply, set to online if not. -
				raise ValueError("`{}` status is not supported, try instead: {}".format(self.configuration.read(category="overview", key="discord.status.set"), ', '.join(list(statuses.keys()))));
			else:	 
				status = statuses[self.configuration.read(category="overview", key="discord.status.set")];
				# - End of custom status assign. -
			
			# - Assingning custom activity status to bot -
			activity = ''
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
				activity = random.choice(activities['list']).format(guildsCount = str(len([guild.id for guild in self.guilds])), membersCount = str(sum([len([m for m in guild.members if not m.bot]) for guild in self.guilds])), helpCommand = '/help')
				if activities['type'] == 'playing': # - Set special statuses: 'Playing something' or 'Watching something' etc. -
					await self.change_presence(status=status, activity=discord.Game(activity));
				elif activities['type'] in list(activitiesList.keys()):
					await self.change_presence(status=status, activity=discord.Activity(type=activitiesList[activities['type']], name=activity));
				else:
					raise ValueError("{} is not a valid activity type".format(activities['type']));
			else:
				await self.change_presence(status=status, activity = None); # - Change only status if activities are not meant to be set -

			self.log.hard('- - - - - - - - - - - APPLICATION ONLINE - - - - - - - - - - -')
			self.log.notify('{} guilds; status: {}; activity: {}'.format(str(len([guild.id for guild in self.guilds])), status, activity if activity else 'None'))
			if self.configuration.read(category="overview", key="discord.activity.set") and self.configuration.read(category="overview", key="discord.activity.cycle"):
				self.log.notify("Activity changing from pool: {} in interval: {}".format(', '.join(activities['list']), self.configuration.read(category="overview", key="discord.activity.cycle-interval")));
				self.loop.create_task(self.cycleStatus(activities = activities, interval = self.configuration.read(category="overview", key="discord.activity.cycle-interval"), status = status))

			# - Sync slash commands tree to global -
			#await self.tree.sync()
		except Exception as e:
			self.log.error(getattr(e, 'message', repr(e)))
			traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
			
	async def cycleStatus(self, activities, interval, status):
		try:
			activitiesList = { "watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening} # - Available activities types, `playing` not included due to diffrent setup procedure -
			await self.wait_until_ready()
			while not self.is_closed():
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
				activity = random.choice(activities['list']).format(guildsCount = str(len([guild.id for guild in self.guilds])), membersCount = str(sum([len([m for m in guild.members if not m.bot]) for guild in self.guilds])), helpCommand = '/help')
				self.log.notify("Next activity: {}; Waiting {} seconds.".format(activity, time))
				await asyncio.sleep(time) # - Wait interval. -
				if activities['type'] == 'playing': # - Set special statuses: 'Playing something' or 'Watching something' etc. -
					await self.change_presence(status=status, activity=discord.Game(activity));
				elif activities['type'] in list(activitiesList.keys()):
					await self.change_presence(status=status, activity=discord.Activity(type=activitiesList[activities['type']], name=activity));
		except Exception as error:
			self.log.error(getattr(e, 'message', repr(e)))
