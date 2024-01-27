import os

import discord
from discord.ext import commands

from frequency.frequency import Frequency

from aiohttp import ClientSession
import asyncpg
import asyncio


async def main():
	"""
	Todo:
		* Fill in extensions
	"""
	async with ClientSession() as web, asyncpg.create_pool(user='postgres', command_timeout=30) as pool:
		
		async with Frequency(
				command_prefix=commands.when_mentioned, extensions=[], pool=pool, web=web, intents=discord.Intents.all()) as bot:
			await bot.start(os.environ.get("TOKEN", ""))

			
asyncio.run(main())
