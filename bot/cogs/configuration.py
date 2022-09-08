import discord
from discord import app_commands, Embed
from discord.ext import commands

class Configuration(app_commands.Group, name="configuration", description="Bots basic configuration commands."): # commands.GroupCog
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		super().__init__()
    
	@app_commands.command(name="refresh")
	@commands.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction, data: str) -> None:
		""" Refresh guild data for service configuration """
		embed = Embed(title="User information",
				colour = ctx.author.colour,
				#timestamp=get_time()
				)
		embed.set_thumbnail(url=self.client.avatar_url)
		embed.add_field( name=chr(173), value="Provided by [lukaqueres](https://github.com/lukaqueres)", inline=True),
		embed.set_footer(text="Provided by [lukaqueres](https://github.com/lukaqueres)")
		await interaction.response.send_message(f"Hello from refresh {data}", ephemeral=True)
		
	@app_commands.command(name="show")
	@commands.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction, data: str) -> None:
		""" Show configuration data """
		await interaction.response.send_message(f"Hello from show {data}", ephemeral=True)
		
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Configuration(bot))
