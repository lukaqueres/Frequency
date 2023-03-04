import discord
import logging
import os
import json

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

	async def __on_voice_channel_join(self, member, after):
		f_channels = self.client.database.select(table="vchannels_manage",
		                                           columns=["function_channels", ],
		                                           **{"guild_id": member.guild.id})
		f_channels = {int(guild_id): settings for guild_id, settings in f_channels["function_channels"].items()}
		if after.channel.id in list(f_channels.keys()):  # - Voice channel is saved as function -
			new_channel = await member.guild.create_voice_channel(name=f"{member.name}'s",
			                                                      category=after.channel.category,
			                                                      reason=f"Voice channel especially for user {member.name}")
			await member.move_to(new_channel, reason=f"Created {member.name}'s channel")
			self.client.database.insert(table="vchannels",
			                            **{
				                            "id": new_channel.id,
				                            "guild_id": member.guild.id,
			                                "owner_id": member.id
			                            })
		else:
			print("not for create")  # - Channel is not for channel creation -

	async def __on_voice_channel_leave(self, member, before):
		data = self.client.database.select(table="vchannels",
		                                   columns=["id", ],
		                                   **{"id": before.channel.id})
		if data is not None:
			if len(before.channel.members) == 0:
				self.client.database.delete(table="vchannels",
				                            **{"id": before.channel.id})
				await before.channel.delete(reason="Channel is empty")

	@commands.Cog.listener()
	async def on_voice_state_update(self, member, before, after):
		if not self.client.database.select(table="vchannels_manage", columns=["enable", ], **{"guild_id": member.guild.id}):
			return  # - Voice channels management is disabled -
		if before.channel is None and after.channel is not None:  # - Joined to channel -
			await self.__on_voice_channel_join(member, after)
		elif before.channel is not None and after.channel is None:  # - Left the channel -
			await self.__on_voice_channel_leave(member, before)
		else:  # - Channel WAS changed -
			pass

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
