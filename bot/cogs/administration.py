import discord, json, os

class Administration(commands.Cog):
	def __init__(self, client):
		self.client = client
  
def setup(client):
	client.add_cog(Administration(client))
