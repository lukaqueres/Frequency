import discord, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot, PIEmbed
from packets.database import Database
from packets.utilities import Configuration

from views.tickets import TicketFunctions, TicketLaunchView, TicketManageView, TicketCloseConfirmView	
	
class Ticket:
	def __init__(self, interaction: discord.Interaction, user: Optional[discord.Member] = None) -> None:
		self.database = Database()
		self.configuration = Configuration()
		self.interaction = interaction
		self.user = user or interaction.user
		self.name = self.__ticketName(self.user)
		self.channel_category = interaction.channel.category
		
	async def __respond_to_interaction(self, content:str, ephemeral: bool = True):	
		try:
			await self.interaction.response.send_message(content = content, ephemeral = ephemeral)
			return True
		except discord.errors.InteractionResponded:
			interaction.edit_original_response(content = content)
			return True
		return False
	
	def __message(self, message:str) -> str:
		messages = {
			"error_disabled": ">>> Tickets creation in this guild is currently disabled",
			"error_already_exists": ">>> Ticket already exists in {ticket_mention}",
			"creating_ticket": ">>> Creating ticket {ticket_name}",
			"error_creating_ticket": ">>> Ticket creation failed, please check bot permissions",
			"ticket_mention_users": ">>> Ticket with: @here"
		}
		return messages[message];
	
	def __ticketName(self, user: discord.Member) -> str:
		syntax = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_name_syntax' ], condition = { "guild_id": interaction.guild.id }) # TODO: Change column to correct one
		syntax.format(userName = user.name.lower().replace(' ', '-'), userDiscriminator = user.discriminator)
		return syntax
		
	def __create_overwrites(self) -> dict:
		ticketRoles = self.database.select(table = 'guilds.tickets', columns = [ 'enabled' ], condition = { "guild_id": interaction.guild.id }) # TODO: Change column to correct one
		moderatorRights = discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
		overwrites = {
			self.interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
			self.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
			self.interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True),
		}
		for roleId in ticketRoles:
			role = interaction.guild.get_role(roleId)
			overwrites[role] = moderatorRights
		return overwrites;
	
	def __already_exists(self) -> bool:
		ticket = utils.get(self.interaction.guild.text_channels, name=self.name)
		if ticket is not None:
			return ticket
		else:
			return False 
		
	async def create(self) -> None:
		if not self.database.select(table = 'guilds.tickets', columns = [ 'enabled' ], condition = { "guild_id": interaction.guild.id }):
			return await self.__respond_to_interaction(content = self.__message("error_disabled"), ephemeral = True)
		
		await self.__respond_to_interaction(content = self.__message("creating_ticket").format(ticket_name = self.name), ephemeral = True)
		ticket = self.__already_exists()
		if ticket: return await self.__respond_to_interaction(content = self.__message("error_already_exists").format(ticket_mention = ticket.mention), ephemeral = True);
		overwrites = self.__create_overwrites();
		try: channel = await self.interaction.guild.create_text_channel(name = self.name, overwrites = overwrites, category = self.channel_category, reason = f"As a ticket for user {member.name} #{member.discriminator}")
		except: return await self.__respond_to_interaction(content = self.__message("error_creating_ticket"), ephemeral = True)
		ping = await channel.send(content = self.__message("ticket_mention_users"));
		await ping.delete() # CD FROM HERE
		title = f"Ticket with {self.user.name}"
		description = "Here you can talk to staff without disturbing"
		embed = PIEmbed(title = title, description = description)
		embed.timestamp = None
		await channel.send(embed = embed, view = TicketManageView());
		await self.__respond_to_interaction(content = f">>> Your ticket's channel has been created here: {channel.mention}")
	
	async def close(self, interaction: discord.Interaction) -> None:
		ticketPrefix = "ticket"
		if (ticketPrefix + '-') in interaction.channel.name:
			title = "Confirm ticket's closure"
			description = "After confirmation ticket will be closed with channel removed"
			embed = PIEmbed(title = title, description = description)
			embed.timestamp = None
			await interaction.response.send_message(embed = embed, view = TicketCloseConfirmView(), ephemeral = True)
		else:
			await interaction.response.send_message("Current channel is not a ticket", ephemeral = True)
class Tickets(commands.Cog): #app_commands.Group
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
		self.functions = TicketFunctions(client.database)
		
	def __channel_is_ticket(self, channel) -> bool:
		ticketPrefix = "ticket"
		return (ticketPrefix + '-') in channel.name
	
	def __user_can_throw_out(self, action_member, target_membed) -> bool:
		ticketPrefix = "ticket"
		return (ticketPrefix + '-') in channel.name
	
	
	#tree = app_commands.CommandTree(self.client)
	ticket = app_commands.Group(name="ticket", description="Tickets for guild users and admin contact.")
	
	@app_commands.context_menu( name = "Open a Ticket" )
	async def open_ticket_context_menu(interaction: discord.Interaction, member: discord.Member):
		await self.functions.create_ticket(interaction = interaction, for_member = member)
	
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
		try:
			await self.functions.close_ticket(interaction = interaction)
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
	
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
