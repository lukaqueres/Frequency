import json, os, discord

from typing import Optional
from discord.ext import commands, tasks
# - Import database in case of error -
from packets.database import Database
from packets.time import Time
from packets.test import Test
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
		self.set_author(name=self.__appName())
		self.color = discord.Color.blurple() # - Assign color `blurple` as an (PI)Embed color. Pretty nice I think  -
		
	def __footerText(self): # - Create footer text from app name from JSON -
		text = f'Provided by {self.__appName()}'; # - Make nice text, so apart from nick name, everything will SCREAM `PLAN IT`, `PLAN IT`... khem, just make footer text, can be changed -
		return text;
	def __appName(self):
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file and fetch app name. -
			configuration = json.load(c); 
			appName = configuration['name'];
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
		
	def field(self, index: Optional[int] = None, name: Optional[str] = None, value: Optional[str] = None, inline: Optional[bool] = False):
		if len(self.embed.fields) == self.field_limit:
			return False # - Return False if fileld limit reached TODO: Raise exception `fields limit reached` -
		if not name and not value:
			self.emptyField(index);
		print(f'title: {len(name)}, content: {len(content)}')
		if len(name) > self.name_limit:
			name = name[0:self.title_limit]; # - Cut field name to fit limit. TODO: Add error for such cases -
		values = [];
		if len(value) > self.value_limit:
			print(f'timesx: {(len(value) // self.value_limit) + 1}');
			for x in range((len(value) // self.value_limit) + 1):
				divide = len(value) // ((len(value) // self.content_limit) + 1)
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

class PIEmbedTest(Test):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.testName = "Lorem Ipsum is simply dummy text of the printing and typesetting industry.";
		self.testValue = """
		Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
		Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and 
		scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, 
		remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
		and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
		It is a long established fact that a reader will be distracted by the readable content ofapagewhenlookingatitslayout.ThepointofusingLoremIpsumisthatithasamore-or-lessnormaldistributionofletters, as opposed to using 'Content here, 
		content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as 
		their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have 
		evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
		Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, 
		making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more 
		obscureLatinwords,consectetur,fromaLoremIpsumpassage,andgoingthroughthecitesofthewordinclassicalliterature,discovered 
		theundoubtablesource.LoremIpsumcomesfromsections1.10.32and1.10.33of"deFinibusBonorumetMalorum"(The Extremes of Good and Evil) 
		by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, 
		"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
		The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" 
		by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
		""";
		
	def execute(self):
		embed = PIEmbed(
			title="PIEmbed",
			description="Test."
		);
		embed.add.field(title=self.testName, content=self.testValue); # - TODO: Finish test -
			
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
