import discord, json
from discord import app_commands
from discord.ext import commands
from typing import Optional

from packets.discord import PIEmbed

class CommandOnCooldown(commands.CommandError):
	def __init__(self, command, cooldown, Optional[interaction], Optional[ctx], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.command = command
		self.cooldown = cooldown
		self.interaction = interaction or None
		self.ctx = ctx or None

class NotEnoughBotPermissions(commands.CommandError):
	def __init__(self, permission, Optional[interaction], Optional[ctx], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.permission = permission
		self.interaction = interaction or None
		self.ctx = ctx or None

class NotEnoughUserPermissions(commands.CommandError):
	def __init__(self, user, permission, Optional[interaction], Optional[ctx], *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.user = user
		self.permission = permission
		self.interaction = interaction or None
		self.ctx = ctx or None
