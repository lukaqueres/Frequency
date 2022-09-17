import discord, json, os

from discord.ext import commands

class Administration(commands.Cog):
	def __init__(self, client: commands.Bot) -> None:
		self.client = client
  
async def setup(client: commands.Bot) -> None:
	await client.add_cog(Administration(client))
