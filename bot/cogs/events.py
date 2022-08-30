import discord, json, os

from datetime import datetime, date, timedelta, timezone
from discord.ext import commands

from packets.time import Time
from packets.database import Database

class Events(commands.Cog):
	def __init__(self, client):
		self.client = client

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
			configuration = json.load(c); 
			log = configuration['developer']['log'];
			defaults = configuration['values']['defaults'];
		if log['notices']:
			print(f'Joined guild: {guild.name}; {guild.id}');
		members = len([m for m in guild.members if not m.bot]); # - Get members count excluding bots. -
		#date_of_join = str("{") + get_time("DD") + str("}")
		time = Time();
		roles = {};
		test = "will see how it will handle these ' and \" quotes, also if it will modify these \\\' and \\\" ! ";
		testtwo = self.client.database.escape.string(test);
		print(test);
		print(testtwo);
		for r in guild.roles:
			if r != guild.default_role:
				roles[r.id] = self.client.database.adapt.string(r.name); # - Adapting string to don't cause errors while inputting to DB. TODO: Do something to indicate that it was addapted. -
		payload = { "id": guild.id,
			   "properties": {
				   "prefix": defaults['prefix'], # - TODO: Check what to do to input string containing ' or ", then maybe add name field -
				   "joined": time.today(),
				   "language": defaults['language']
			   },
			   "roles": roles,
		};
		self.client.database.insert(table = 'guilds',
					    payload = payload);
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
			configuration = json.load(c); 
			log = configuration['developer']['log'];
		if log['notices']:
			print(f'Left guild: {guild.name}; {guild.id}')
		self.client.database.delete(table = 'guilds',
					    condition = {"id": guild.id});
    
def setup(client):
	client.add_cog(Events(client))