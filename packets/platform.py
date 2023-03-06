import discord
import os
import doctest
import random
import asyncio
import logging.config

from config.config import Configuration
from dependencies.database.database import Database

from discord import Colour
from discord.ext import commands

from views.VCConsole import VCConsoleView

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


class PIBot(commands.Bot):

	activities = {"watching": discord.ActivityType.watching, "listening": discord.ActivityType.listening,
				"playing": "playing"}
	statuses = {"online": discord.Status.online,
				"offline": discord.Status.offline,
				"idle": discord.Status.idle,
				"dnd": discord.Status.dnd}

	def __init__(self, **kwargs):
		super().__init__(command_prefix=self.__get_prefix, intents=discord.Intents.all(), **kwargs)

		self.database = Database(os.environ.get('DATABASE_URL'))
		self.config = Configuration("client", "general")

		self.restrict_guild = discord.Object(id=self.config.get("general", "dev.restrict"))
		self.synced_views = False

	async def setup_hook(self):
		self.tree.copy_global_to(guild=self.restrict_guild)
		await self.tree.sync()

	def __get_prefix(self, client: discord.Client, message: discord.Message):
		# record = self.database.select(table='guilds', columns=['prefix', ], **{"id": message.guild.id})
		record = self.database.select(table="guilds", columns=["prefix", ], limit=1, **{"id": message.guild.id})
		if not record:
			record = {"prefix": "$"}
		return record["prefix"]

	def __sync_views(self):

		if not self.synced_views:
			self.add_view(VCConsoleView())
			self.synced_views = True
		else:
			pass

	async def on_ready(self):
		self.__sync_views()

		logger.info(f"Instance of {self.user.name} loaded")
		logger.info(f"Active {len(self.guilds)} guilds")

		status = self.statuses[self.config.get("client", "status")]
		logger.debug(f"Status: {status}")
		preset = self.config.get("client", "activity-preset")
		if not preset:
			logger.debug("No activity preset used")
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
		if activity["type"] == "playing":
			await self.change_presence(status=status, activity=discord.Game(name))
		else:
			await self.change_presence(status=status, activity=discord.Activity(type=activity["type"], name=name))
		if activity["interval"]:
			self.loop.create_task(self.cycle_status())

	async def cycle_status(self):
		await self.wait_until_ready()
		while not self.is_closed():
			preset = self.config.get("client", "activity-preset")
			preset = self.config.get("client", f"activities.{preset}")
			activity = dict(type=self.activities[preset["type"]])
			status = self.statuses[self.config.get("client", "status")]
			activity.update(name=random.choice(preset["list"]))
			interval = preset["cycle-interval"]
			intervals = {"long": random.randrange(25199, 36001), "short": random.randrange(1800, 7200)}
			interval = interval if isinstance(interval, int) else intervals[interval]
			await asyncio.sleep(interval)
			logger.debug(activity)
			if activity["type"] == "playing":
				await self.change_presence(status=status, activity=discord.Game(activity["name"]))
			else:
				await self.change_presence(status=status, activity=discord.Activity(type=activity["type"],
																				name=activity["name"]))


class PIEmbed(discord.Embed):

	colors = {
		"blue": Colour.blue(),
		"blurple": Colour.blurple(),
		"brand_green": Colour.brand_green(),
		"brand_red": Colour.brand_red(),
		"dark_blue": Colour.dark_blue(),
		"dark_gold": Colour.dark_gold(),
		"dark_gray": Colour.dark_gray(),
		"dark_green": Colour.dark_green(),
		"dark_grey": Colour.dark_grey(),
		"dark_magenta": Colour.dark_magenta(),
		"dark_orange": Colour.dark_orange(),
		"dark_purple": Colour.dark_purple(),
		"dark_red": Colour.dark_red(),
		"dark_teal": Colour.dark_teal(),
		"dark_theme": Colour.dark_theme(),
		"darker_gray": Colour.darker_gray(),
		"darker_grey": Colour.darker_grey(),
		"default": Colour.default(),
		"fuchsia": Colour.fuchsia(),
		"gold": Colour.gold(),
		"green": Colour.green(),
		"greyple": Colour.greyple(),
		"light_gray": Colour.light_gray(),
		"light_grey": Colour.light_grey(),
		"lighter_gray": Colour.lighter_gray(),
		"lighter_grey": Colour.lighter_grey(),
		"magenta": Colour.magenta(),
		"og_blurple": Colour.og_blurple(),
		"orange": Colour.orange(),
		"purple": Colour.purple(),
		"random": Colour.random(),
		"red": Colour.red(),
		"teal": Colour.teal(),
		"yellow": Colour.yellow(),
	}

	limits = {
		"total": 6000,
		"title": 256,
		"description": 4096,
		"fields": 25,
		"field.name": 256,
		"field.value": 1024,
		"footer.text": 2048,
		"author.name": 256
	}

	def __init__(self, **kwargs):
		super().__init__(**kwargs)

	def validate(self) -> bool:  # TODO: Make it nicer
		if len(self) > self.limits.get("total"):
			return False
		if self.title:
			if len(self.title) > self.limits.get("title"):
				return False
		if self.description:
			if len(self.description) > self.limits.get("description"):
				return False
		if self.fields:
			if len(self.fields) > self.limits.get("fields"):
				return False
			for field in self.fields:
				if len(field.name) > self.limits.get("field.name"):
					return False
				if len(field.value) > self.limits.get("field.value"):
					return False
		if self.footer:
			if len(self.footer.text) > self.limits.get("author.name"):
				return False
		if self.author:
			if len(self.author.name) > self.limits.get("author.name"):
				return False
		return True

	@staticmethod
	def confirm(**kwargs):
		arguments = {"color": Colour.red(),
		             "title": "Confirm"
		             }
		arguments.update(kwargs)
		embed = PIEmbed(**arguments)
		return embed

	@staticmethod
	def vc_console(**kwargs):
		embed = PIEmbed(title="Voice channel control panel",
		                description="Simple way to manage your current voice channel")
		embed.add_field(name="`🖊️` Rename", value=chr(173))
		embed.add_field(name="`👥` Limit", value=chr(173))
		embed.add_field(name="`✔️` Allow", value=chr(173))
		embed.add_field(name="`🔉` Mute / Unmute", value=chr(173))
		embed.add_field(name="`🔒` Lock / Unlock", value=chr(173))
		embed.add_field(name="`🔄` Transfer", value=chr(173))
		embed.add_field(name="`📤` Kick", value=chr(173))
		embed.add_field(name="`✖️` Disallow", value=chr(173))
		embed.add_field(name="`🗑️` Close", value=chr(173))
		return embed
