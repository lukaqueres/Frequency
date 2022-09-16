import discord
from discord import app_commands
from discord.ext import commands

from packages.discord import PIBot 

class Checks:
	def __init__(self, client: PIBot) -> None:
		self.client = client

	def is_admin(self):
		def predicate(interaction: discord.Interaction = Null, ctx: commands.Context = Null):
			if ctx:
				return ctx.message.author.guild_permissions.administrator
			else:
				return interaction.user.guild_permissions.administrator
		return commands.check(predicate)
