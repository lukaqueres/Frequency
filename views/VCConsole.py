import discord

from typing import Optional


class VCConsoleView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout=None)

	@discord.ui.button(emoji="➕", style=discord.ButtonStyle.blurple, custom_id="create_vc_button")
	async def create_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="✖️", style=discord.ButtonStyle.red, custom_id="delete_vc_button")
	async def delete_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass
