import discord


class UserNotInVoice(discord.app_commands.AppCommandError):
	pass


class VCConsoleView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout=None)

	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		if interaction.user.voice.channel is not None:
			raise UserNotInVoice
		channel = self.client.database.select(table="vchannels",
		                                         columns=["owner_id", ],
		                                         **{"id": interaction.user.voice.channel.id})
		return True


	@discord.ui.button(emoji=discord.PartialEmoji.from_str("pencil:1082733750573604864"),
	                   style=discord.ButtonStyle.blurple,
	                   custom_id="rename_vc_button")
	async def rename_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		await interaction.response.send_message("edit")

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("people:1082733793602981908"),
	                   style=discord.ButtonStyle.blurple,
	                   custom_id="limit_vc_button")
	async def limit_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("checkmarkcircle:1082740747897425961"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="allow_vc_button")
	async def allow_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("volumemute:1082733813089714196"),
	                   style=discord.ButtonStyle.blurple,
	                   custom_id="un_mute_vc_button")
	async def mute_unmute_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("lockclosed:1082733831079067780"),
	                   style=discord.ButtonStyle.blurple,
	                   custom_id="un_lock_vc_button")
	async def lock_unlock_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("sync:1082733869586993182"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="transfer_vc_button")
	async def transfer_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("personremove:1082733730147340328"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="kick_from_vc_button")
	async def kick_from_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("removecircle:1082740766499152004"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="disallow_to_vc_button")
	async def disallow_to_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("personadd:1082733699570880604"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="invite_to_vc_button")
	async def invite_to_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass

	@discord.ui.button(emoji=discord.PartialEmoji.from_str("closecircle:1082733909592260708"),
	                   style=discord.ButtonStyle.red,
	                   custom_id="close_vc_button")
	async def close_channel_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass
