import discord, datetime, os, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIEmbed
from packets.database import Database

class PIView(discord.ui.View):
	def __init__(self, timeout : Optional[float] = None) -> None:# : Optional[float] 
		super().__init__(timeout = timeout)
		self.database = Database()

class PITextInput(discord.ui.TextInput):
	def __init__(self, **kwargs):
        	# The placeholder is what will be shown when no option is chosen
        	# The min and max values indicate we can only pick one of the three options
        	# The options parameter defines the dropdown options. We defined this above
		super().__init__(label = "Reason", style=discord.TextStyle.short, custom_id = "ticket_reason_of_close_input", placeholder="Input reason for ticket close", default=None, required=False, min_length=0, max_length=100, row=2)
		#super().__init__(**kwargs)
	
	async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
		await interaction.response.send_message(f'Your input is {self.value}')
