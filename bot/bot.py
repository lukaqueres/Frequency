# - Importing required unspecified packages -
import json, os, random, asyncio, traceback, sys
from random import randrange, randint

# - Importing discord packages -
import discord
from discord.ext import commands, tasks
from discord import Intents, app_commands


# - Importing in-project packages -
from packets.database import Database
from packets.discord import PIBot

# - Import cog as a part of slash not-sync work-around -
#from cogs.configuration import ConfigurationGroup


intents = discord.Intents.all() # - Get all Intents TODO: Remember to get messages and other permissions that require discord approval after verification -
# bot = client = commands.Bot(command_prefix = prefix, intents=intents); # - Old client setup, moved to custom class instead -
client = PIBot()

# >---------------------------------------< COMMANDS >---------------------------------------< # 
		
@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Displays ping!"""
    await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}', ephemeral = True) # interaction.user.mention

# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
async def startup():
	if self.configuration.read(category="utilities", key="developer.extensions.load"):
		loaded = []; # - Extensions loaded succesfully -
		failed = []; # - Extensions failed to load -
		for cog in os.listdir(self.configuration.read(category="utilities", key="developer.extensions.directory")):
			if cog.endswith('.py'):	 # - Every file from directory path with .py extension is threated as cog. -
				if not cog[:-3] in self.configuration.read(category="utilities", key="developer.extensions.ignore"):
					try:
						await client.load_extension(f"{self.configuration.read(category="utilities", key="developer.extensions.directory")}.{cog[:-3]}");
						loaded.append(cog[:-3]);
					except Exception as e: # - Catch exception in loading, can be extended. -
						failed.append([cog[:-3], getattr(e, 'message', repr(e))]);
				else:
					failed.apped([cog[:-3], 'Extension ignored.']);
		if len(loaded) != 0:
			client.log.notify(f"Extensions loaded ({len(loaded)}): {', '.join(str(l) for l in loaded)}"); # - Log loaded cogs with it's number and list. -
		if len(failed) != 0:
			client.log.notify(f"Failed to load ({len(failed)}) extensions: {', '.join(str(f[0] + ': ' + f[1]) for f in failed)}"); # - Log failed cogs with it's number and list. -
		
		async with client:
			TOKEN = os.environ.get('TOKEN')
			await client.start(TOKEN)

asyncio.run(startup());
#if __name__ == "__main__":
#	client.run(TOKEN)
		
