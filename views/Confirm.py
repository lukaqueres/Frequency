import discord

from typing import Callable


class ConfirmView(discord.ui.View):
	def __init__(self, callback: Callable, callback_attr: dict) -> None:
		super().__init__(timeout=60.0)
		self.callback = callback
		self.callback_attr = callback_attr
		self.cancel_message = ">>> Action revoked"

	@discord.ui.button(emoji="✔️", label="Confirm", style=discord.ButtonStyle.green, custom_id="confirm_confirm")
	async def confirm_confirm_button(self, interaction: discord.Interaction, button: discord.ui.button):
		for child in button.view.children:
			child.disable = True
		button.view.stop()
		self.callback_attr.update({"interaction": interaction})
		await self.callback(**self.callback_attr)

	@discord.ui.button(emoji="✖️", label="Cancel", style=discord.ButtonStyle.red, custom_id="confirm_cancel")
	async def confirm_cancel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		for child in button.view.children:
			child.disable = True
		button.view.stop()
		await interaction.response.send_message(self.cancel_message, ephemeral=True)
