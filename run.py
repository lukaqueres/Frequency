# >---------------------------------------< Imports >---------------------------------------< #

# - Importing required external packages -
import asyncio
import os
import logging
from typing import Final
# - Importing discord packages -
import discord
from discord import app_commands

# - Importing in-project packages -
from packets.platform import PIBot

client = PIBot()

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")

# >---------------------------------------< COMMANDS >---------------------------------------< #


@client.tree.command(name="ping", description="Returns instance ping")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Ping: `{round(client.latency * 1000)}`',
                                            ephemeral=True)  # interaction.user.mention


# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
async def startup():
    if client.config.get("general", key="extensions.load"):
        loaded = []
        failed = []
        directory = client.config.get("general", key="extensions.dir")
        for cog in os.listdir(directory):
            if cog.endswith(".py"):
                if not cog[:-3] in client.config.get("general", key="extensions.ignore"):
                    try:
                        await client.load_extension(f"{directory}.{cog[:-3]}")
                        loaded.append(cog[:-3])
                    except Exception as e:
                        failed.append([cog[:-3], getattr(e, 'message', repr(e))])
                        logger.warning(f"Loading of cog {cog[:-3]} failed")
                else:
                    failed.append([cog[:-3], 'Extension ignored.'])
        if len(loaded) != 0:
            logger.info(
                f"Extensions loaded ({len(loaded)}): {', '.join(str(l) for l in loaded)}")
        if len(failed) != 0:
            logger.info(
                f"Failed to load ({len(failed)}) extensions: {', '.join(str(f[0] + ': ' + f[1]) for f in failed)}")

    async with client:
        token: Final[str] = os.environ.get('TOKEN')
        await client.start(token)  # - Just run this BITCH -


asyncio.run(startup())
