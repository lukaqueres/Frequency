import discord, json
from discord import app_commands, Embed
from discord.ext import commands

from packets.time import Time

class Configuration(app_commands.Group, name="configuration", description="Bots basic configuration commands."): # commands.GroupCog
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
		super().__init__()
    
	@app_commands.command(name="refresh")
	@commands.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction) -> None:
		""" Refresh guild data for service configuration """
		with open('configuration.json', 'r') as c: # - Open 'configuration.json' file containing work data. Fetch extensions load & log details. -
			configuration = json.load(c); 
			appName = configuration['name'];
		embed = Embed(title="User information",
				colour = interaction.user.colour,
				timestamp=Time.UTCNow()
				)
		embed.set_thumbnail(url=self.client.user.avatar)
		embed.add_field( name=chr(173), value="Made by [lukaqueres](https://github.com/lukaqueres)", inline=True),
		embed.set_footer(text=f"Provided by {appName}")
		await interaction.response.send_message(embed=embed, ephemeral=True)
		
	@app_commands.command(name="show")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction) -> None:
		""" Show configuration data """
		await interaction.response.send_message("Hello from show", ephemeral=True)
		
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Configuration(client))
