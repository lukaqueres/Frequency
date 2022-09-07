import discord
from discord import app_commands
from discord.ext import commands

class Configuration(commands.GroupCog, name="configuration", description="Bots basic configuration commands."):
	def __init__(self, bot: commands.Bot) -> None:
		self.bot = bot
		super().__init__()
    
	@app_commands.command(name="refresh")
	@app_commands.check.has_permissions(administrator = True)
	async def conf_sub_refresh(self, interaction: discord.Interaction, data: str) -> None:
		""" /parent sub-1 """
		await interaction.response.send_message(f"Hello from refresh {data}", ephemeral=True)
		
	@app_commands.command(name="show")
	@app_commands.check.has_permissions(administrator = True)
	async def conf_sub_show(self, interaction: discord.Interaction, data: str) -> None:
		""" /parent sub-2 """
		await interaction.response.send_message(f"Hello from show {data}", ephemeral=True)
		
async def setup(bot: commands.Bot) -> None:
	await bot.add_cog(Configuration(bot))
