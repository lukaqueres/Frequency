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
			raise CommandOnCooldown(command = interaction.command, cooldown = round(retry, 1), interaction = interaction);
    
	async def cog_command_error(self, ctx, error):
		if isinstance(error, CommandOnCooldown):
			if error.interaction:
				return await interaction.response.send_message(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
			if error.ctx:
				return await ctx.send(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
			print(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
		else:
			# All other Errors not returned come here. And we can just print the default TraceBack.
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	
	@app_commands.command(name="refresh", description="Check for accurate & refresh guild data for service configuration")
	@commands.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		#self.__commands_check(interaction);
		""" Check for accurate & refresh guild data for service configuration """
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
		embed = PIEmbed(
			title="Configuration",
			description="Guild data synchronize check will be performed before refreshing records."
		);
		embed.set_thumbnail(url=self.client.user.avatar)
		
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
			await interaction.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(name="show", description="Show configuration data")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		self.__commands_check(interaction);
		""" Show configuration data """
		await interaction.response.send_message("Hello from show", ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Configuration(client))
