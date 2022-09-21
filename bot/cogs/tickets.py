import discord, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot, PIEmbed
from views.tickets import TicketLaunchView, TicketManageView, TicketCloseConfirmView	
	
class Tickets(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
		
	def __channel_is_ticket(self, channel) -> bool:
		ticketPrefix = "ticket"
		return (ticketPrefix + '-') in channel.name
	
	def __user_can_throw_out(self, action_member, target_membed) -> bool:
		ticketPrefix = "ticket"
		return (ticketPrefix + '-') in channel.name
	
	ticket = app_commands.Group(name="ticket", description="Tickets for guild users and admin contact.")
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="setup", description="Send embed with button allowing ticket creation.")
	async def tickets_set_ticket_creation_channel(self, interaction: discord.Interaction) -> None:
		title = "Use button below to create a ticket"
		description = "Clicking button will create channel with you and guild staff for conversation"
		embed = PIEmbed(title = title, description = description)
		embed.timestamp = None
		await interaction.channel.send(embed = embed, view = TicketLaunchView())
		await interaction.response.send_message(">>> Setup completed. You can disable/enable tickets by using `/ticket toggle`", ephemeral = True)
	
	@cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="close", description="Close current ticket.")
	async def ticket_delete(self, interaction: discord.Interaction) -> None:
		ticketPrefix = "ticket"
		if (ticketPrefix + '-') in interaction.channel.name:
			title = "Confirm ticket's closure"
			description = "After confirmation ticket will be closed with channel removed"
			embed = PIEmbed(title = title, description = description)
			embed.timestamp = None
			await interaction.response.send_message(embed = embed, view = TicketCloseConfirmView(), ephemeral = True)
		else:
			await interaction.response.send_message("Current channel is not a ticket", ephemeral = True)
	
	@cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="toggle", description="Toggle creation of new tickets, can be enabled/disabled.")
	async def tickets_enable_or_disable(self, interaction: discord.Interaction) -> None:
		pass;
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="create", description="Create new ticket with guild contact team.")
	@app_commands.describe( member='Create ticket with member assigned. Guild staff only.' )
	async def ticket_create(self, interaction: discord.Interaction, member: Optional[discord.Member] = None) -> None:
		pass;
	
	@cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="add", description="Add member to current ticket.")
	@app_commands.describe( member='Guild member to add to ticket.' )
	async def ticket_add_member_to_ticket(self, interaction: discord.Interaction, member: discord.Member) -> None:
		ticketPrefix = "ticket"
		if (ticketPrefix + '-') in interaction.channel.name:
			await interaction.channel.set_permissions(member, view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
			await interaction.response.send_message(f">>> User {member.mention} was added to current ticket by {interaction.user.mention}", ephemeral = True)
		else:
			await interaction.response.send_message("Current channel is not a ticket", ephemeral = True)
	
	@cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="remove_member", description="Remove member from ticket.")
	@app_commands.describe( member='Guild member to remove from ticket.' )
	async def ticket_remove_member_from_ticket(self, interaction: discord.Interaction, member: discord.Member) -> None:
		ticketPrefix = "ticket"
		moderatorId = 1020060418871414824
		ticketModerator = interaction.guild.get_role(moderatorId)
		if (ticketPrefix + '-') in interaction.channel.name:
			if ticketModerator not in interaction.user.roles: return await interaction.response.send_message("Only moderators can remove users from ticket", ephemeral = True)
			if ticketModerator in member.roles: return await interaction.response.send_message("Can't remove staff from ticket", ephemeral = True)
			await interaction.channel.set_permissions(member, overwrite = None)
			await interaction.response.send_message(f">>> User {member.mention} was removed from current ticket by {interaction.user.mention}", ephemeral = True)
		else:
			await interaction.response.send_message("Current channel is not a ticket", ephemeral = True)

async def setup(client: PIBot) -> None:
	await client.add_cog(Tickets(client))
