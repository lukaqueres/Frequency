import discord, json
from discord import app_commands, Embed
from discord.ext import commands

from packets.time import Time
from packets.discord import PIEmbed

class Configuration(app_commands.Group, name="configuration", description="Bots basic configuration commands."): # commands.GroupCog
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		super().__init__()
    
	@app_commands.command(name="refresh")
	@commands.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		""" Check for accurate & refresh guild data for service configuration """
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
		embed = PIEmbed(
			title="Configuration",
			description="Guild data synchronize check will be performed before refreshing records."
		);
		embed.set_thumbnail(url=self.client.user.avatar)
		
		DBValues = self.client.database.select(
			table='guild.properties', 
			condition = {"id": interaction.guild_id}, 
			columns = ["roles"]);
		if DBValues:
			guildRoles = {};
			for r in interaction.guild.roles:
				if r != interaction.guild.default_role:
					guildRoles[r.id] = r.name;
			if DBValues == guildRoles:
				embed.add_field( name="Roles", value="**Accurate**", inline=False);
			else:
				embed.add_field( name="Roles", value="**Synchronized**", inline=False);
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(name="show")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		""" Show configuration data """
		await interaction.response.send_message("Hello from show", ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Configuration(client))
