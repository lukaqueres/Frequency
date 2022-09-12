import discord, json
from discord import app_commands
from discord.ext import commands

from packets.time import Time
from packets.discord import PIEmbed
from packets.error import CommandOnCooldown

class Configuration(commands.Cog):
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		
	@app_commands.command(name="debugping")
	async def pingConf(self, interaction: discord.Interaction) -> None:
		"""Displays ping!"""
		await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}') # interaction.user.mention

class ConfigurationGroup(app_commands.Group, name="configuration", description="Bots basic configuration commands."): # commands.GroupCog
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.guild)
		super().__init__()
		
	def __commands_check(self, interaction: discord.Interaction, **kwargs):
		retry = self.cooldown.get_bucket(interaction.message).update_rate_limit();
		if retry:
			print('on cooldown')
			interaction.response.send_message(message=f">>> Command`{interaction.command}` is now on cooldown, try again in `{round(retry, 1)}s`.")
			raise CommandOnCooldown(command = interaction.command, cooldown = round(retry, 1), interaction = interaction);
		else:
			print('no cooldown')
			return True;
	"""
	async def cog_command_error(self, interaction, error):
		if isinstance(error, CommandOnCooldown):
			if error.interaction:
				return await interaction.response.send_message(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
			if error.ctx:
				return await ctx.send(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
			print(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
		else:
			# All other Errors not returned come here. And we can just print the default TraceBack.
			print('Ignoring exception in command {}:'.format(interaction.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	"""
	@app_commands.command(name="refresh", description="Check for accurate & refresh guild data for service configuration")
	@commands.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		dfhhdfff[][sddadsd90sdad';
		if not self.__commands_check(interaction):
			return print('stopping')
		""" Check for accurate & refresh guild data for service configuration """
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
			log = configuration['developer']['log'];
			defaults = configuration['values']['defaults'];
		embed = PIEmbed(
			title="Configuration",
			description="Guild data synchronize check will be performed before refreshing records."
		);
		embed.set_thumbnail(url=self.client.user.avatar)
		dfhhdfff[][sddadsd90sdad';
		DBRoles = self.client.database.select(
			table = 'guilds.properties', 
			condition = {"id": interaction.guild_id}, 
			columns = ["roles"]);
		if DBRoles:
			guildRoles = {};
			for r in interaction.guild.roles:
				if r != interaction.guild.default_role and not r.managed:
					guildRoles[r.id] = r.name;
			DBRoles = {int(k): v for k, v in DBRoles.items()} # - After SELECT keys are string instead of int, failing `==` -
			print(f'DBRoles: {DBRoles}');
			print(f'guildRoles: {guildRoles}');
			DBrefresh = False;
			if len(DBRoles) == len(guildRoles):
				for k, v in DBRoles.items():
					if guildRoles[k] == v:
						print(f'k: {k}');
					else:
						DBrefresh = True;
						break;
				
			else:
				DBrefresh = True;
			print(f'DBrefresh: {DBrefresh}');
			if DBrefresh:
				payload = {"roles": guildRoles};
				self.client.database.update(
					table = 'guilds.properties', 
					payload = payload, 
					condition = {"id": interaction.guild.id}
				);
				embed.add_field( name="Roles", value="*Synchronized*", inline=False);
			else:
				embed.add_field( name="Roles", value="*Accurate*", inline=False);
			print('Interaction respond')
		else:
			if log['notices']:
				print(f'By configuration joined guild: {guild.name}; {guild.id}');
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
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(name="show", description="Show configuration data")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		self.__commands_check(interaction);
		""" Show configuration data """
		await interaction.response.send_message("Hello from show", ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Configuration(client))
