import logging
import asyncio
import os


async def startup():
	logging_format = logging.Formatter('%(asctime)s : %(name)s - %(levelname)s : %(message)s', '%d-%m-%y %H:%M:%S')
	discord_handler, http_handler = [logging.StreamHandler()]*2
	discord_handler.setLevel(logging.DEBUG)
	discord_handler.setFormatter(logging_format)

	http_handler.setLevel(logging.INFO).setFormatter(logging_format)

	logging.getLogger('discord').addHandler(discord_handler)
	logging.getLogger('discord.http').addHandler(http_handler)

	async with client:
		token: Final[str] = os.environ.get('TOKEN')
		await client.start(token)  # - Just run this BITCH -

asyncio.run(startup())
