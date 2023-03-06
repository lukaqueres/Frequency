import discord

class VCConsoleView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout=None)

	@discord.ui.button(emoji="🖊️", style=discord.ButtonStyle.blurple, custom_id="rename_vc_button")
	async def rename_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="👥", style=discord.ButtonStyle.blurple, custom_id="limit_vc_button")
	async def limit_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="✔️", style=discord.ButtonStyle.red, custom_id="allow_vc_button")
	async def allow_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="🔉", style=discord.ButtonStyle.blurple, custom_id="un_mute_vc_button")
	async def mute_unmute_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="🔒", style=discord.ButtonStyle.blurple, custom_id="un_lock_vc_button")
	async def lock_unlock_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="🔄", style=discord.ButtonStyle.red, custom_id="transfer_vc_button")
	async def transfer_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="📤", style=discord.ButtonStyle.red, custom_id="kick_from_vc_button")
	async def kick_from_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="✖️", style=discord.ButtonStyle.red, custom_id="disallow_to_vc_button")
	async def disallow_to_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="📥", style=discord.ButtonStyle.red, custom_id="invite_to_vc_button")
	async def invite_to_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji="🗑️", style=discord.ButtonStyle.red, custom_id="close_vc_button")
	async def close_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass
