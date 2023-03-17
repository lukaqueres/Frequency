import discord
import logging
import os
import json

from discord.ext import commands
from discord import app_commands
from typing import Optional

from config.config import Configuration
from packets.platform import PIBot
from packets.platform import PIEmbed

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


def cooldown_except_admin(interaction: discord.Interaction) -> Optional[app_commands.Cooldown]:
	if interaction.permissions.administrator:
		return None
	return app_commands.Cooldown(1, 10.0)


config = Configuration("general")


class Embeds(commands.Cog):
	"""

	@note Here are all color codes: https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812
	"""

	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client

	embeds = app_commands.Group(name="embed", description="Embed writing and management")

	# @app_commands.guild_only()
	# @app_commands.checks.dynamic_cooldown(cooldown_except_admin)
	# @app_commands.checks.has_permissions(manage_messages=True)
	# @embeds.command(name="write", description="Send an embed with given parameters")
	# @app_commands.describe(title="Title of created embed", description="Description of embed")
	# async def write(self, interaction: discord.Interaction, title: str, description: str) -> None:
	# 	embed = discord.Embed(title=title, description=description)
	# 	await interaction.response.send_message(embed=embed)

	@app_commands.guild_only()
	@app_commands.checks.dynamic_cooldown(cooldown_except_admin)
	@app_commands.checks.has_permissions(manage_messages=True)
	@embeds.command(name="send", description=f"Sends an embed from JSON file generated on {config.get('general', 'site')}")
	async def send(self, interaction: discord.Interaction, file: discord.Attachment) -> None:
		data = json.loads(await file.read())
		embed = PIEmbed.from_dict(data=data)
		if not embed.validate():
			embed = PIEmbed(title="Bad request",
			        description=f"Invalid embed, some elements may be too long. \n",
	                color=discord.Color.gold())
			embed.add_field(name=chr(173), value=f"You can create new file at [theplanbot.com]({config.get('general','site')})")
			return await interaction.response.send_message(embed=embed, ephemeral=True)
		if data["user"]:
			webhook = await interaction.channel.create_webhook(name=f"Embed for {interaction.user.name}",
												reason=f"To send embed as a response to {interaction.user.name} request")
			try:
				await webhook.send(username=data["user"]["name"], avatar_url=data["user"]["avatar"] or None, embed=embed)
			except Exception as e:
				raise e
			finally:
				await webhook.delete(reason=f"Embed sent as a response to {interaction.user.name} request")
		else:
			await interaction.channel.send(embed=embed)
		embed = PIEmbed(title="Embed sent",
		                description=f"Created based on `{file.filename}` file. \n",
		                color=discord.Color.gold())
		embed.add_field(name=chr(173), value=f"You can create new file at [theplanbot.com]({config.get('general', 'site')})")
		await interaction.response.send_message(embed=embed, ephemeral=True)

	# @write.error
	@send.error
	async def on_embed_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
		if isinstance(error, app_commands.CommandOnCooldown):
			return await interaction.response.send_message(str(error), ephemeral=True)
		elif isinstance(error, app_commands.errors.MissingPermissions):
			return await interaction.response.send_message(str(error), ephemeral=True)
		else:
			logger.error(error)
			return await interaction.response.send_message("There was an error while processing command", ephemeral=True)


async def setup(client: PIBot) -> None:
	await client.add_cog(Embeds(client))
