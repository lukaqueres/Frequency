import discord, json, os

from datetime import datetime, date, timedelta, timezone
from discord.ext import commands

from packets import time;

class Events(commands.Cog):
	def __init__(self, client):
		self.client = client

    @commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
			configuration = json.load(c); 
			log = configuration['developer']['log'];
		if log['notices']:
			print(f'Joined guild: {guild.name};')
		defaults = {'prefix': '$', 'langugage': 'eng'};
		members = len([m for m in guild.members if not m.bot]); # - Get members count excluding bots. -
		#date_of_join = str("{") + get_time("DD") + str("}")
		time = Time();
		roles = {}
		for r in guild.roles:
			if r != guild.default_role:
				roles[r.id] = r.name;
		payload = { "id": guild.id,
			   properties = {
				   "prefix": defaults['prefix'],
				   "name": guild.name,
				   "joined": time.today();
			   },
			   channels = {},
			   roles = roles,
			   features = {}
		};
		self.client.database.insert(table = 'guilds',
					    payload = payload);
    
    
def setup(client):
	client.add_cog(Events(client))
