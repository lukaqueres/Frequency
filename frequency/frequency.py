from __future__ import annotations

import configparser
import logging
from typing import Optional

import asyncpg
from aiohttp import ClientSession

import discord
from discord.ext import commands


class Frequency(commands.Bot):
	
	def __init__(self, *args, extensions: list[str], pool: asyncpg.Pool, web: ClientSession, guild: Optional[str] = None, **kwargs):
		"""
		Frequency class constructor.
		
		Sort of jumpstarts commands.Bot instance

		Args:
			*args: arguments for commands.Bot constructor
			extensions: List of cog names, loaded on startup
			pool: postgres connection pool, uses asyncpg.Pool object
			web: aiohttp ClientSession object, mandatory
			guild: Optional test guild id
			**kwargs: kwargs for commands.Bot constructor. Should contain command_prefix and intents
		"""
		super().__init__(*args, **kwargs)
		
		# Services
		self.__pool: asyncpg.Pool = pool
		self.__web: ClientSession = web
		
		# Operation
		self.__extensions: list[str] = extensions
		self.__guild: Optional[str] = guild
	
	async def setup_hook(self) -> None:
		for extension in self.__extensions:
			await self.load_extension(extension)
		
		if self.__guild:
			guild = discord.Object(self.__guild)
			self.tree.copy_global_to(guild=guild)
			await self.tree.sync(guild=guild)
		else:
			await self.tree.sync()
	
	# This would also be a good place to connect to our database and
	# load anything that should be in memory prior to handling events.
	
	async def on_ready(self) -> None:
		pass
	