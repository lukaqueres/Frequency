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
		if log['notices']:
			print(f'Joined guild: {guild.name}; {guild.id}')
		defaults = {'prefix': '$', 'langugage': 'eng'};
		members = len([m for m in guild.members if not m.bot]); # - Get members count excluding bots. -
		#date_of_join = str("{") + get_time("DD") + str("}")
		time = Time();
		roles = {};
		for r in guild.roles:
			if r != guild.default_role:
				roles[r.id] = r.name;
		payload = { "id": guild.id,
			   "properties": {
				   "prefix": defaults['prefix'],
				   "joined": time.today()
			   },
			   "channels": {},
			   "roles": roles,
			   "features": {}
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
