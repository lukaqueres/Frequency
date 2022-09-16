import discord, json, os

from datetime import datetime, date, timedelta, timezone
from discord.ext import commands

from packets.time import Time
from packets.database import Database

class Events(commands.Cog):
	def __init__(self, client: commands.Bot) -> None:
		self.client = client

# - Guilds - - - - - - - - - - Guilds related events - - - - - - - - - -

	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
			configuration = json.load(c); 
			log = configuration['developer']['log'];
			defaults = configuration['values']['defaults'];
		if log['notices']:
			print(f'Joined guild: {guild.name}; {guild.id}');
		members = len([m for m in guild.members if not m.bot]); # - Get members count excluding bots. -
		time = Time();
		roles = {};
		for r in guild.roles:
			if r != guild.default_role and not r.managed:
				#roles[r.id] = self.client.database.escape.string(r.name); # - Adapting string to don't cause errors while inputting to DB. TODO: Do something to indicate that it was addapted. -
				roles[r.id] = r.name;
		payload = { "id": guild.id,
			"prefix": defaults['prefix'], # - TODO/DONE/: Check what to do to input string containing ' or ", then maybe add name field -
			"language": defaults['language'],
			"roles": roles,
		};
		self.client.database.insert(table = 'guilds.properties',
					    payload = payload);
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		with open('./configuration.json', 'r') as c: # - Open 'configuration.json' json file. Getting logging details. -
			configuration = json.load(c); 
			log = configuration['developer']['log'];
		if log['notices']:
			print(f'Left guild: {guild.name}; {guild.id}')
		self.client.database.delete(table = 'guilds.properties',
					    condition = {"id": guild.id});

# - Roles - - - - - - - - - - Roles related events - - - - - - - - - -

	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		guildRoles = {};
			for r in role.guild.roles:
				if r != role.guild.default_role and not r.managed:
					guildRoles[r.id] = r.name;
		payload = {"roles": guildRoles};
		self.client.database.update(
			table = 'guilds.properties', 
			payload = payload, 
			condition = {"id": role.guild.id}
		);
		
	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		guildRoles = {};
			for r in role.guild.roles:
				if r != role.guild.default_role and not r.managed:
					guildRoles[r.id] = r.name;
		payload = {"roles": guildRoles};
		self.client.database.update(
			table = 'guilds.properties', 
			payload = payload, 
			condition = {"id": role.guild.id}
		);
		
	@commands.Cog.listener()
	async def on_guild_role_update(self, before, after):
		role = after;
		guildRoles = {};
			for r in role.guild.roles:
				if r != role.guild.default_role and not r.managed:
					guildRoles[r.id] = r.name;
		payload = {"roles": guildRoles};
		self.client.database.update(
			table = 'guilds.properties', 
			payload = payload, 
			condition = {"id": role.guild.id}
		);
    
async def setup(client):
	await client.add_cog(Events(client))
