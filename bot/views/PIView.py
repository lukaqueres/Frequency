import discord, datetime, os, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIEmbed
from packets.database import Database

class PIView(discord.ui.View):
	def __init__(self, timeout = None) -> None:# : Optional[float] 
		super().__init__(timeout)
		self.database = Database()
