import discord

from packets.database import Database

class Events(commands.Cog): # - Events handle cog -
	def __init__(self, client: commands.Bot) -> None:
		self.client = client

# - Guilds - - - - - - - - - - Guilds related events - - - - - - - - - -
	
	# - When bot joins guild - 
	@commands.Cog.listener()
	async def on_guild_join(self, guild) -> None:
		self.client.log.notify(f'Joined guild: {guild.name}; {guild.id}');
		self.client.database.predefined.add_new_guild(guild);
		
	# - When bot if thrown out of guild ( sad :[ ) - 
	@commands.Cog.listener()
	async def on_guild_remove(self, guild) -> None:
		self.client.log.notify(f'Left guild: {guild.name}; {guild.id}');
		self.client.database.predefined.remove_guild(guild);

# - Roles - - - - - - - - - - Roles related events - - - - - - - - - -
	
	# - Fetch roles from guild -
	def fetch_roles(self, role) -> dict:
		roles = {};
		for r in role.guild.roles:
			if r != role.guild.default_role and not r.managed: # - Ignore bots self roles -
				roles[r.id] = r.name;
		return roles;

	# - On creating new role -
	@commands.Cog.listener()
	async def on_guild_role_create(self, role) -> None:
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
		
	# - When deleting existing role -
	@commands.Cog.listener()
	async def on_guild_role_delete(self, role) -> None:
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
		
	# - On role update ( name change, permissions update ) -
	@commands.Cog.listener()
	async def on_guild_role_update(self, before, after) -> None:
		role = after; # - Because only thing this event does for now is update guild roles in DB, choose role after change -
		self.client.database.predefined.update_roles(guild, self.fetch_roles(role));
    
async def setup(client):
	await client.add_cog(Events(client))
