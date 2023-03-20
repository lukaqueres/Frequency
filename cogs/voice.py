import os
import logging
import discord
import sys
import traceback

from enum import Enum
from typing import Optional, Union

from discord.ext import commands
from discord import app_commands

from packets.platform import PIBot

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


class InvalidVoiceChannel(commands.CommandError):
	"""Exception for cases of invalid Voice Channels."""


class Voice(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client

	voice = app_commands.Group(name="voice", description="Music management & playing")

	play_sources = [app_commands.Choice(name=s, value=s) for s in ["Youtube", "Spotify"]]

	class Sources(Enum):
		Youtube = "yt"
		Spotify = "sp"

	@app_commands.guild_only()
	@voice.command(name="play", description=f"Plays song from Spotify or YouTube")
	@app_commands.describe(source='Source that will be searched for provided title',
	                       url='Url of song or playlist to be played',
	                       title='Title of song that will be searched for'
	                       )
	async def play(self, interaction: discord.Interaction, url: Optional[str], title: Optional[str], source: Optional[Sources]):
		return await interaction.response.send_message(content=source, ephemeral=True)
		pass

	@voice.command(name="connect", description=f"Connects to given channel or to user")
	async def connect(self, interaction: discord.Interaction, channel: Optional[Union[discord.VoiceChannel, discord.StageChannel]]):
		if not channel:
			channel = interaction.user.voice.channel if interaction.user.voice else None
		if not channel:
			raise InvalidVoiceChannel("Invalid voice channel or user not in voice channel.")
		return await interaction.response.send_message(content=channel.name, ephemeral=True)


async def setup(client: PIBot) -> None:
	await client.add_cog(Voice(client))
