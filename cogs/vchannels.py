import discord
import logging
import os
import json

from typing import Optional

from discord.ext import commands
from discord import app_commands

from packets.platform import PIBot
from packets.platform import PIEmbed

from views.VCConsole import VCConsoleView
from views.Confirm import ConfirmView

logging.config.fileConfig(fname=os.environ.get("LOG_CONFIG"), disable_existing_loggers=False)
logger = logging.getLogger("logger")


class VChannels(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
		self.functional_channels_limit = 2

	vChannels = app_commands.Group(name="vchannels", description="Voice channels management")

	async def __on_voice_channel_join(self, member, after):
		f_channels = self.client.database.select(table="vchannels_manage",
		                                         columns=["function_channels", ],
		                                         **{"guild_id": member.guild.id})
		f_channels = {int(guild_id): settings for guild_id, settings in f_channels["function_channels"].items()}
		if after.channel.id in list(f_channels.keys()):  # - Voice channel is saved as function -
			f_channel = f_channels[after.channel.id]
			new_channel = await after.channel.clone(name=f"{member.name}'s",
			                                        reason=f"Voice channel especially for user {member.name}")
			new_channel = await new_channel.edit(category=after.channel.category,
			                                     reason=f"Adjust {member.name}'s channel properties")
			await member.move_to(new_channel, reason=f"Created {member.name}'s channel")
			self.client.database.insert(table="vchannels",
			                            **{"id": new_channel.id,
			                               "guild_id": member.guild.id,
			                               "owner_id": member.id
			                               })
			if f_channel["console"]:
				await new_channel.send(content=f">>> Hey {member.mention}! Here you can manage your new channel", delete_after=300.0)
				embed = PIEmbed.vc_console()
				await new_channel.send(embed=embed, view=VCConsoleView())
		else:
			pass  # - Channel is not for channel creation -

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
		elif before.channel.id != after.channel.id:  # - Changed the channel -
			await self.__on_voice_channel_leave(member, before)
			await self.__on_voice_channel_join(member, after)
		else:  # - Something not channel related -
			pass

	@app_commands.guild_only()
	@app_commands.checks.has_permissions(manage_channels=True)
	@vChannels.command(name="console", description=f"Creates console for voice channel management")
	async def console(self, interaction: discord.Interaction) -> None:
		embed = PIEmbed.vc_console()
		await interaction.channel.send(embed=embed, view=VCConsoleView())
		await interaction.response.send_message(content="```Console sent```", ephemeral=True)

	@app_commands.guild_only()
	@app_commands.checks.has_permissions(manage_channels=True)
	@vChannels.command(name="functional", description=f"Sets functional voice channel with various functions")
	async def functional(self, interaction: discord.Interaction,
	                     channel: discord.VoiceChannel, console: Optional[bool] = False) -> None:
		f_channels = self.client.database.select(table="vchannels_manage",
		                                         columns=["function_channels", ],
		                                         **{"guild_id": interaction.guild.id})
		f_channels = {int(guild_id): settings for guild_id, settings in f_channels["function_channels"].items()}
		if channel.id not in list(f_channels.keys()):
			await self.__add_function(interaction=interaction, channel=channel, channel_attrs={"console": console})
		else:
			embed = PIEmbed.confirm(title=f"Do you want to remove function from channel?",
			                description=f"If you confirm, function from `{channel.name}` channel will be deleted")
			await interaction.response.send_message(embed=embed, view=ConfirmView(callback=self.__remove_function,
			                                                                      callback_attr={"channel": channel},
			                                                                      ),
			                                        ephemeral=True)

	async def __add_function(self, interaction: discord.Interaction, channel: discord.VoiceChannel, channel_attrs: dict):
		f_channels = self.client.database.select(table="vchannels_manage",
		                                         columns=["function_channels", ],
		                                         **{"guild_id": interaction.guild.id})
		f_channels = {int(guild_id): settings for guild_id, settings in f_channels["function_channels"].items()}
		if len(list(f_channels.keys())) >= self.functional_channels_limit and channel.id not in list(f_channels.keys()):
			embed = PIEmbed(title="Function channels at capacity",
			                description=f"To set function on `{channel.name}` channel you have to remove one of the existing")
			for key, settings in f_channels.items():
				embed.add_field(name=f"Channel `{settings['name']}`", value=f"Task: {settings['function']}", inline=False)
			return await interaction.response.send_message(embed=embed)
		channel_attrs.update({"name": channel.name, "function": "clone"})
		f_channels.update({channel.id: channel_attrs})
		self.client.database.update(table="vchannels_manage",
		                            values={"function_channels": json.dumps(f_channels)},
		                            **{"guild_id": interaction.guild.id})
		await interaction.response.send_message(content=f">>> Added function to `{channel.name}` channel", ephemeral=True)

	async def __remove_function(self, interaction: discord.Interaction, channel: discord.VoiceChannel):
		f_channels = self.client.database.select(table="vchannels_manage",
		                                         columns=["function_channels", ],
		                                         **{"guild_id": interaction.guild.id})
		f_channels = {int(guild_id): settings for guild_id, settings in f_channels["function_channels"].items()}
		f_channels.pop(channel.id, None)
		self.client.database.update(table="vchannels_manage",
		                            values={"function_channels": json.dumps(f_channels)},
		                            **{"guild_id": interaction.guild.id})
		await interaction.response.send_message(content=f">>> Removed function from `{channel.name}` channel", ephemeral=True)


async def setup(client: PIBot) -> None:
	await client.add_cog(VChannels(client))
