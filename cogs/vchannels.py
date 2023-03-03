import discord
import logging
import os

from discord.ext import commands
from discord import app_commands

from packets.platform import PIBot
from packets.platform import PIEmbed

from views.VCConsole import VCConsoleView

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


class VChannels(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client

	vChannels = app_commands.Group(name="voice", description="Voice channels management")

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if not self.client.database.select(table="vchannels_manage", columns=["enable", ]):
			return  # - Voice channels management is disabled -
		if not before.channel or not after.channel or before.channel.id == after.channel.id:  # - Channel was not changed -
			pass
		else:  # - Channel WAS changed -
			channel_a_id = self.client.database.select(table="vchannels_manage",
			                                           columns=["create_channel_a_id", ],
			                                           **{"guild_id": member.guild.id})
			if after.channel.id == channel_a_id:
				new_channel = await member.guild.create_voice_channel(name=f"{member.name}'s",
				                                       category=after.channel.category,
				                                       reason=f"Voice channel especially for user {member.name}")
				await member.move_to(new_channel, reason="Created new channel")
			else:
				pass  # - Channel is not for channel creation -

	@app_commands.guild_only()
	@app_commands.checks.has_permissions(manage_channels=True)
	@vChannels.command(name="console", description=f"Creates console for voice channel management")
	async def console(self, interaction: discord.Interaction) -> None:
		embed = PIEmbed(title="Voice channels control panel",
		                description="Here you can manage your current voice channel")
		await interaction.channel.send(embed=embed, view=VCConsoleView())
		await interaction.response.send_message(content="```Console sent```", ephemeral=True)


async def setup(client: PIBot) -> None:
	await client.add_cog(VChannels(client))
