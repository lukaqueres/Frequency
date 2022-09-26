# - Importing required exeternal packages -
import os, asyncio, traceback, sys

# - Importing discord packages -
import discord
from discord import app_commands


# - Importing in-project packages -
from packets.discord import PIBot

client = PIBot()

# - Prepare file system -

if not os.path.exists("tallies/"):
	os.makedirs("tallies/")

# >---------------------------------------< COMMANDS >---------------------------------------< # 
		
@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Displays ping!"""
    await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}', ephemeral = True) # interaction.user.mention

# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
async def startup():
	if client.configuration.read(category="overview", key="developer.extensions.load"): # - If load extensions (cogs)-
		loaded = []; # - Extensions loaded succesfully -
		failed = []; # - Extensions failed to load -
		for cog in os.listdir(client.configuration.read(category="overview", key="developer.extensions.directory")):
			if cog.endswith('.py'):	 # - Every file from directory path with .py extension is handled as a potential cog. -
				if not cog[:-3] in client.configuration.read(category="overview", key="developer.extensions.ignore"): # - If cog is not ignored ( in ignored list ) -
					try: # - Try to load extensions, allow to load extensions with error without abort -
						await client.load_extension(f"{client.configuration.read(category='overview', key='developer.extensions.directory')}.{cog[:-3]}");
						loaded.append(cog[:-3]);
					except Exception as e: # - Catch exception in loading, can be extended. -
						failed.append([cog[:-3], getattr(e, 'message', repr(e))]);
						traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
				else:
					failed.apped([cog[:-3], 'Extension ignored.']); # - Ignored cog -
		if len(loaded) != 0: # - If there is no loaded not show -
			client.log.notify(f"Extensions loaded ({len(loaded)}): {', '.join(str(l) for l in loaded)}"); # - Log loaded cogs with it's number and list. -
		if len(failed) != 0: # - Show only if there is anything to show -
			client.log.notify(f"Failed to load ({len(failed)}) extensions: {', '.join(str(f[0] + ': ' + f[1]) for f in failed)}"); # - Log failed cogs with it's number and list. -
		
	async with client: 
		TOKEN = os.environ.get('TOKEN')
		await client.start(TOKEN) # - Just run this BITCH -

asyncio.run(startup());
