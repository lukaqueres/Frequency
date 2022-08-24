import discord, json, os

from discord.ext import commands

class Administration(commands.Cog):
	def __init__(self, client):
		self.client = client
  
def setup(client):
	client.add_cog(Administration(client))
