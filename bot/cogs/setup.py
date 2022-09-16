import discord, json
from discord import app_commands
from discord.ext import commands

from packets.time import Time
from packets.discord import PIEmbed
from packets.error import CommandOnCooldown

class ConfigurationGroup(commands.Cog):
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		
	@app_commands.command(name="debugping")
	async def pingConf(self, interaction: discord.Interaction) -> None:
		"""Displays ping!"""
		await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}') # interaction.user.mention

		
class Setup(commands.Cog): # commands.GroupCog / app_commands.Group
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.guild)
		super().__init__()
		
	setup = app_commands.Group(name="setup", description="Setup - specified commands.")
		
	async def __commands_check(self, interaction: discord.Interaction, **kwargs):
		if not interaction.user.guild_permissions.administrator:
			await interaction.response.send_message(content=f">>> Command `{interaction.command.name}` requires user to have administrator privilege.", ephemeral=True)
			return False;
		retry = self.cooldown.get_bucket(interaction).update_rate_limit();
		if retry:
			await interaction.response.send_message(content=f">>> Command `{interaction.command.name}` is now on cooldown, try again in `{round(retry, 1)}s`.", ephemeral=True)
			return False;
			#raise CommandOnCooldown(command = interaction.command.name, cooldown = round(retry, 1), interaction = interaction);
		else:
			return True;
	"""	
	async def cog_command_error(self, interaction, error):
		if isinstance(error, CommandOnCooldown):
			if error.interaction:
				return await interaction.response.send_message(content=f">>> Command `{interaction.command.name}` is now on cooldown, try again in `{round(retry, 1)}s`.", ephemeral=True)
			
			if error.ctx:
				return await ctx.send(f">>> Command `{interaction.command.name}` is now on cooldown, try again in `{round(retry, 1)}s`.")
			print(f"Command `{error.command}` is on cooldown, try again in `{error.cooldown}`s.")
	"""		
	#@commands.has_permissions(administrator = True)
	@setup.command(name="refresh", description="Check for accurate & refresh guild data for service setup")
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		if not await self.__commands_check(interaction):
			return;
		""" Check for accurate & refresh guild data for service configuration """
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
			log = configuration['developer']['log'];
			defaults = configuration['values']['defaults'];
		embed = PIEmbed(
			title="Setup",
			description="Refresh"
		);
		#embed.set_thumbnail(url=self.client.user.avatar)
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
			DBrefresh = False;
			if len(DBRoles) == len(guildRoles):
				for k, v in DBRoles.items():
					if guildRoles[k] == v:
						pass;
					else:
						DBrefresh = True;
						break;
				
			else:
				DBrefresh = True;
			if DBrefresh:
				payload = {"roles": guildRoles};
				self.client.database.update(
					table = 'guilds.properties', 
					payload = payload, 
					condition = {"id": interaction.guild.id}
				);
				rolesStatus = "*Synchronized*"
			else:
				rolesStatus = "*Accurate*"
			embed.add.field(name = "Record", value = rolesStatus, inline = False)
		else:
			if log['notices']:
				print(f'By configuration joined guild: {interaction.guild.name}; {interaction.guild.id}');
			members = len([m for m in interaction.guild.members if not m.bot]); # - Get members count excluding bots. -
			time = Time();
			roles = {};
			for r in interaction.guild.roles:
				if r != interaction.guild.default_role and not r.managed:
					#roles[r.id] = self.client.database.escape.string(r.name); # - Adapting string to don't cause errors while inputting to DB. TODO: Do something to indicate that it was addapted. -
					roles[r.id] = r.name;
			payload = { "id": interaction.guild.id,
				"prefix": defaults['prefix'], # - TODO/DONE/: Check what to do to input string containing ' or ", then maybe add name field -
				"language": defaults['language'],
				"roles": roles,
			};
			self.client.database.insert(table = 'guilds.properties',
					    payload = payload);
			embed.add.field(name = "Record", value = "Updated", inline = False)
			
		await interaction.response.send_message(embed=embed, ephemeral=True)
	"""
	@setup.command(name="show", description="Show configuration data")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		self.__commands_check(interaction);
		await interaction.response.send_message("Hello from show", ephemeral=True)
	"""
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Setup(client))
