# >---------------------------------------< Imports >---------------------------------------< #

# - Importing required external packages -
import asyncio, os, traceback, sys
from typing import Final
# - Importing discord packages -
import discord
from discord import app_commands

# - Importing in-project packages -
from packets.platform import PIBot

client = PIBot()


# >---------------------------------------< COMMANDS >---------------------------------------< #


@client.tree.command()
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Ping: {round(client.latency * 1000)}',
                                            ephemeral=True)  # interaction.user.mention


# >---------------------------------------< COGS / EXTENSIONS LOAD >---------------------------------------< # 
async def startup():
    async with client:
        token: Final[str] = os.environ.get('TOKEN')
        await client.start(token)  # - Just run this BITCH -


asyncio.run(startup())
