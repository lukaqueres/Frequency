import discord
import os
import doctest
import random
import asyncio
import logging as log

from config.config import Configuration
from dependencies.database.database import Database

from discord.ext import commands

log.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', datefmt='%d-%m-%y %H:%M:%S')
logger = log.getLogger('base_logger')


class PIBot(commands.Bot):

	activities = {"watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening}
	statuses = {"online": discord.Status.online,
				"offline": discord.Status.offline,
				"idle": discord.Status.idle,
				"dnd": discord.Status.dnd}

	def __init__(self, **kwargs):
		super().__init__(command_prefix=self.__get_prefix, intents=discord.Intents.all(), **kwargs)

		self.database = Database(os.environ.get('DATABASE_URL'))
		self.config = Configuration("client", "config")

		self.synced_views = False

	def __get_prefix(self, client: discord.Client, message: discord.Message):
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
		self.__sync_views()

		status = self.statuses[self.config.get("client", "status")]

		preset = self.config.get("client", "activity-preset")
		if not preset:
			return await self.change_presence(status=status)
		preset = self.config.get("client", f"activities.{preset}")
		if preset["type"] and len(preset["list"]) < 1:
			raise KeyError("Activity type requires any message")
		try:
			activity = {"type": self.activities[preset["type"]]}
		except KeyError:
			raise KeyError(f"Type {preset['type']} is not valid discord activity type")
		except Exception as e:
			raise e
		activity.update(interval=preset["cycle-interval"])
		activity.update(list=preset["list"])
		name = random.choice(activity["list"])
		await self.change_presence(status=status, activity=discord.Activity(type=activity["type"], name=name))
		logger.info(f"Instance of {self.user.name} loaded")
		if activity["interval"]:
			self.loop.create_task(self.cycle_status())

	async def cycle_status(self):
		await self.wait_until_ready()
		while not self.is_closed():
			preset = self.config.get("client", "activity-preset")
			preset = self.config.get("client", f"activities.{preset}")
			activity = {type: self.activities[preset["type"]]}
			status = self.statuses[self.config.get("client", "status")]
			activity.update(name=random.choice(preset["list"]))
			interval = preset["cycle-interval"]
			intervals = {"long": random.randrange(25199, 36001), "short": random.randrange(1800, 7200)}
			interval = interval if isinstance(interval, int) else intervals[interval]
			await asyncio.sleep(interval)
			await self.change_presence(status=status, activity=discord.Activity(type=activity["type"],
																				name=activity["name"]))


doctest.run_docstring_examples(PIBot, globals())
