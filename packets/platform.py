import discord
import os
import doctest
import random

from dependencies.config.config import Configuration
from dependencies.database.database import Database

from discord.ext import commands


class PIBot(commands.Bot):

	def __init__(self, **kwargs):
		super().__init__(command_prefix=self.__get_prefix, intents=discord.Intents.all(), **kwargs)

		self.db = Database(os.environ.get('DATABASE_URL'))
		self.config = Configuration("client", "config")

	def __get_prefix(self, client, message: discord.Message):
		record = self.database.select(table='guilds', columns=['prefix', ], condition={"id": message.guild.id})
		return record["prefix"]

	def __sync_views(self):

		if not self.synced_views:
			# self.add_view(TicketLaunchView())
			# self.add_view(TicketManageView())
			self.synced_views = True
		else:
			pass

	async def on_ready(self):
		activities = {"watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening}
		statuses = {"online": discord.Status.online, "offline": discord.Status.offline, "idle": discord.Status.idle,
		            "dnd": discord.Status.dnd}

		self.__sync_views()

		preset = self.config.get("client", "activity-preset")
		if not preset:
			return
		preset = self.config.get("client", f"activities.{preset}")
		try:
			activity = {"type": activities[preset["type"]]}
		except KeyError:
			raise KeyError(f"Type {preset['type']} is not valid discord activity type")
		except Exception as e:
			raise e
		activity.update(interval=preset["cycle-interval"])
		activity.update(list=preset["list"])
		status = statuses[self.config.get("client", "status")]
		name = random.choice(activity["list"])
		await self.change_presence(status=status, activity=discord.Activity(type=activity["type"], name=name))
		if activity["interval"]:
			self.loop.create_task(self.cyclestatus(list=activity["list"],
			                                       interval=activity["interval"],
			                                       status=status))

	async def cyclestatus(self):
		pass

doctest.run_docstring_examples(PIBot, globals())
