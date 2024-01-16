from __future__ import annotations

import logging

import discord
from discord.ext import commands


class Frequency(commands.Bot):
	def __init__(self, **kwargs):
		super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=discord.Intents.all(), **kwargs)
		
	async def __prefix(self, bot: commands.Bot, message: discord.Message) -> str:
		"""
		
		Args:
			bot:
			message:

		Returns:

		"""
		# TODO: Add custom prefixes
		
		return commands.when_mentioned_or("$")(bot, message)
	