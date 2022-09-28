import discord

from discord.ext import commands
from discord import app_commands

from packets.discord import PIBot

class Information(commands.Cog): #app_commands.Group
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
	
	info = app_commands.Group(name="info", description="Display information & debug data of various objects")
		
async def setup(client: PIBot) -> None:
	await client.add_cog(Information(client)) 
