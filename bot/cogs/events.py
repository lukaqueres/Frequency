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
		self.client.log.notify(f'Joined guild: {guild.name}; {guild.id}');
		self.client.database.predefined.add_new_guild(guild);
		
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		self.client.log.notify(f'Left guild: {guild.name}; {guild.id}');
		self.client.database.predefined.remove_guild(guild);

# - Roles - - - - - - - - - - Roles related events - - - - - - - - - -
	
	def fetch_roles(self, role) -> dict:
		roles = {};
		for r in role.guild.roles:
			if r != role.guild.default_role and not r.managed:
				roles[r.id] = r.name;
		return roles;

	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
		
	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
		
	@commands.Cog.listener()
	async def on_guild_role_update(self, before, after):
		role = after;
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
    
async def setup(client):
	await client.add_cog(Events(client))
