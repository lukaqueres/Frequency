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
		
	async def __commands_check(self, interaction: discord.Interaction, **kwargs):
		retry = self.cooldown.get_bucket(interaction).update_rate_limit();
		if retry:
			print('on cooldown')
			await interaction.response.send_message(content=f">>> Command `{interaction.command.name}` is now on cooldown, try again in `{round(retry, 1)}s`.", ephemeral=True)
			#raise CommandOnCooldown(command = interaction.command, cooldown = round(retry, 1), interaction = interaction);
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
		if not await self.__commands_check(interaction):
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
				embed.add_field( name="Roles", value="*Synchronized*", inline=False);
			else:
				embed.add_field( name="Roles", value="*Accurate*", inline=False);
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
			
		title = ''
		content = """
		Lorem Ipsum is simply dummy text of the printing and typesetting industry. 
		Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and 
		scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, 
		remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, 
		and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
		It is a long established fact that a reader will be distracted by the readable content of a page when looking at its layout. 
		The point of using Lorem Ipsum is that it has a more-or-less normal distribution of letters, as opposed to using 'Content here, 
		content here', making it look like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as 
		their default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various versions have 
		evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the like).
		Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, 
		making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more 
		obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered 
		the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) 
		by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance. The first line of Lorem Ipsum, 
		"Lorem ipsum dolor sit amet..", comes from a line in section 1.10.32.
		The standard chunk of Lorem Ipsum used since the 1500s is reproduced below for those interested. Sections 1.10.32 and 1.10.33 from "de Finibus Bonorum et Malorum" 
		by Cicero are also reproduced in their exact original form, accompanied by English versions from the 1914 translation by H. Rackham.
		"""
		len(title)
		len(content)
		embed.add.field(title="xxxxxxxxxxxfvjufbjnufbsijobunbfjnbfjnbfjnfb", content=content);
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(name="show", description="Show configuration data")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		self.__commands_check(interaction);
		""" Show configuration data """
		await interaction.response.send_message("Hello from show", ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Configuration(client))
