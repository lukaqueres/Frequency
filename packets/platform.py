import discord
import os
import doctest
import random

from config.config import Configuration
from database.db import Database

from discord.ext import commands


class PIBot(commands.Bot):

	def __init__(self, **kwargs):
		super().__init__(command_prefix=self.__get_prefix, intents=discord.Intents.all(), **kwargs)

		self.db = Database(os.environ.get('DATABASE_URL'))
		self.config = Configuration("client", "config")

	def __get_prefix(self, client, message: discord.Message):
		record = self.database.select(table='guilds', columns=['prefix', ], condition={"id": message.guild.id})
		return record["prefix"]

	async def on_ready(self):
		activities = {"watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening}
		statuses = {"online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle,
		            "dnd": discord.Status.dnd}
		preset = self.config.get("client", "activity-preset")
		if preset:
			preset = self.config.get("client", f"activities.{preset}")
			try:
				activity = {"type": activities[preset["type"]]}
			except KeyError as e:
				raise KeyError(f"Type {preset['type']} is not valid discord activity type")
			activity.update(interval=activities[preset["cycle-interval"]])


doctest.run_docstring_examples(PIBot, globals())
