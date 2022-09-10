import discord, json
from discord import app_commands
from discord.ext import commands
from typing import Optional

from packets.discord import PIEmbed

class CommandOnCooldown(commands.CommandError):
    def __init__(self, command, cooldown, Optional(interaction), Optional(ctx), *args, **kwargs):
        self.command = command
        self.cooldown = cooldown
        self.interaction = interaction or None
        self.ctx = ctx or None
        super().__init__(*args, **kwargs)
