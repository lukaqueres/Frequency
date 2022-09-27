import discord, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot, PIEmbed
from packets.database import Database
from packets.utilities import Configuration

from views.tickets import TicketLaunchView, TicketManageView, TicketCloseConfirmView	
	
class Ticket:
	def __init__(self, interaction: discord.Interaction, user: Optional[discord.Member] = None) -> None:
		self.database = Database()
		self.configuration = Configuration()
		self.interaction = interaction
		self.user = user or interaction.user
		self.name = self.__ticketName(self.user)
		self.channel_category = self.__channel_category()
		
	async def __respond_to_interaction(self, content:str, ephemeral: bool = True):	
		try:
			await self.interaction.response.send_message(content = content, ephemeral = ephemeral)
			return True
		except discord.errors.InteractionResponded:
			await self.interaction.edit_original_response(content = content)
			return True
		return False
	
	def __default_text(self, text:str) -> str:
		texts = {
			"new_ticket_embed_title": f"Ticket with `{self.user.name}`",
			"new_ticket_embed_description": "Here you can talk to staff without disturbing",
			"close_ticket_embed_title": "Confirm ticket's closure",
			"close_ticket_embed_description": "After confirmation ticket will be closed with channel removed"
		}
		return texts[text]
	
	def __message(self, message:str) -> str:
		messages = {
			"error_disabled": ">>> Tickets creation in this guild is currently disabled",
			"error_already_exists": ">>> Ticket already exists in {ticket_mention}",
			"creating_ticket": ">>> Creating ticket `{ticket_name}`",
			"error_creating_ticket": ">>> Ticket creation failed, please check bot permissions",
			"ticket_mention_users": ">>> Ticket with: @here"
		}
		return messages[message];
	
	def __channel_category(self):
		categoryId = self.database.select(table = 'guilds.tickets', columns = [ 'tickets_category_id' ], condition = { "guild_id": self.interaction.guild.id })
		if categoryId:
			category = discord.utils.get(self.interaction.guild.categories, id=categoryId)
		else:
			category = self.interaction.channel.category
		return category
	
	def __ticketName(self, user: discord.Member) -> str:
		syntax = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_name_syntax' ], condition = { "guild_id": self.interaction.guild.id })
		name = syntax.format(userName = self.user.name.lower().replace(' ', '-'), userDiscriminator = self.user.discriminator)
		return name
		
	def __create_overwrites(self) -> dict:
		ticketRoles = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_add_roles' ], condition = { "guild_id": self.interaction.guild.id })
		moderatorRights = discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
		overwrites = {
			self.interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
			self.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
			self.interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True),
		}
		if ticketRoles:
			ticketRoles = [int(r) for r in ticketRoles]
			for roleId in ticketRoles:
				role = self.interaction.guild.get_role(roleId)
				overwrites[role] = moderatorRights
		return overwrites;
	
	def __is_ticket_channel(self) -> bool:
		if self.database.select(table = 'guilds.tickets', columns = [ 'store_ticket_channels' ], condition = { "guild_id": self.interaction.guild.id }):
			channels = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_channels_names_and_users_storage' ], condition = { "guild_id": self.interaction.guild.id });
			channels = {int(k): v for k, v in channels.items()}
			if self.interaction.channel.id in list(channels.keys()):
				return True
		else:
			syntax = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_name_syntax' ], condition = { "guild_id": self.interaction.guild.id })
			syntax = syntax.format(userName = ' ', userDiscriminator = ' ')
			syntax = syntax.split(' ')
			for part in syntax:
				print(f'part: {part} is: {part in self.interaction.channel.name}')
				if part in self.interaction.channel.name:
					return True
			return False 
		return False
	
	def __already_exists(self):
		if self.database.select(table = 'guilds.tickets', columns = [ 'store_ticket_channels' ], condition = { "guild_id": self.interaction.guild.id }):
			channels = self.database.select(table = 'guilds.tickets', columns = [ 'ticket_channels_names_and_users_storage' ], condition = { "guild_id": self.interaction.guild.id });
			channels = {int(k): v for k, v in channels.items()}
			for channelId, userId in channels.items():
				if self.user.id == userId:
					ticket = discord.utils.get(self.interaction.guild.text_channels, id=channelId )
					return ticket
				return False
		else:
			ticket = utils.get(self.interaction.guild.text_channels, name=self.name)
			if ticket is not None:
				return ticket
			else:
				return False 
		return False
	
	def __are_tickets_enabled(self):
		return self.database.select(table = 'guilds.tickets', columns = [ 'enabled' ], condition = { "guild_id": self.interaction.guild.id })
	
	async def create(self) -> None:
		if not self.__are_tickets_enabled(): return await self.__respond_to_interaction(content = self.__message("error_disabled"), ephemeral = True)
		ticket = self.__already_exists()
		if ticket: return await self.__respond_to_interaction(content = self.__message("error_already_exists").format(ticket_mention = ticket.mention), ephemeral = True);
		await self.__respond_to_interaction(content = self.__message("creating_ticket").format(ticket_name = self.name), ephemeral = True)
		overwrites = self.__create_overwrites();
		try: channel = await self.interaction.guild.create_text_channel(name = self.name, overwrites = overwrites, category = self.channel_category, reason = f"As a ticket for user {self.user.name} #{self.user.discriminator}")
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		#except: return await self.__respond_to_interaction(content = self.__message("error_creating_ticket"), ephemeral = True)
		ping = await channel.send(content = self.__message("ticket_mention_users"));
		await ping.delete()
		embedContents = self.database.select(table = 'guilds.tickets', columns = [ 'manage_ticket_embed' ], condition = { "guild_id": self.interaction.guild.id })
		embed = PIEmbed(title = embedContents["title"] or self.__default_text("new_ticket_embed_title"), description = embedContents["description"] or self.__default_text("new_ticket_embed_description"))
		embed.timestamp = None
		await channel.send(embed = embed, view = TicketManageView());
		await self.__respond_to_interaction(content = f">>> Your ticket's channel has been created here: {channel.mention}")
	
	async def confirm_close(self) -> None:
		if self.__is_ticket_channel():
			embedContents = self.database.select(table = 'guilds.tickets', columns = [ 'confirm_ticket_close_embed' ], condition = { "guild_id": self.interaction.guild.id }) # - TODO: Check column name -
			embed = PIEmbed(title = embedContents["title"] or self.__default_text("close_ticket_embed_title"), description = embedContents["description"] or self.__default_text("close_ticket_embed_description"))
			embed.timestamp = None
			await self.interaction.response.send_message(embed = embed, view = TicketCloseConfirmView(), ephemeral = True)
		else:
			await self.interaction.response.send_message("Current channel is not a ticket", ephemeral = True)
			
	async def send_ticket_console(self):
		pass
			
	async def generate_tally(self) -> None:
		await self.interaction.response.defer()
		if os.path.exists(f"tallies/{self.interaction.channel.id}.md"):
			return await self.interaction.followup.send(">>> Tally for this ticket is already being inscribed!", ephemeral = True)
		with open(f"tallies/{self.interaction.channel.id}.md", 'a') as f:
			f.write(f"# Tally for ticket in channel {self.interaction.channel.name}:\n\n")
			async for message in self.interaction.channel.history(limit = 500, oldest_first = True):
				created = message.created_at.strftime("%d.%m.%Y at %H:%M:%S")# created = datetime.strftime(message.created_at, "%d.%m.%Y at %H:%M:%S")
				if message.edited_at:
					edited = message.edited_at.strftime("%d.%m.%Y at %H:%M:%S") # edited = datetime.strftime(message.edited_at, "%d.%m.%Y at %H:%M:%S")
					f.write(f"{message.author} on {created}: {message.clean_content} ( Edited at {edited} )\n")
				else:
					f.write(f"{message.author} on {created}: {message.clean_content}\n")
			generated = datetime.datetime.now().strftime("%d.%m.%Y at %H:%M:%S")
			appName = 'Plan It'
			f.write(f"## Tally inscribed by {appName} for {interaction.user.name}\nOn {generated}, Time Zone: UTC")
		with open(f"tallies/{interaction.channel.id}.md", 'rb') as f:
			await interaction.followup.send(file = discord.File(f, f"{self.interaction.channel.name}.md"))
			os.remove(f"tallies/{self.interaction.channel.id}.md")
			
class Tickets(commands.Cog): #app_commands.Group
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
	
	ticket = app_commands.Group(name="ticket", description="Tickets for guild users and admin contact.")
	
	@app_commands.context_menu( name = "Open a Ticket" )
	async def open_ticket_context_menu(interaction: discord.Interaction, member: discord.Member):
		ticket = Ticket(interaction = interaction, user = member)
		await ticket.create()
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="console", description="Console for tickets configuration.")
	async def send_tickets_console(self, interaction: discord.Interaction) -> None:
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
			ticket = Ticket(interaction = interaction, user = member)
			await ticket.confirm_close()
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
	@ticket.command(name="member", description="Add member to current ticket.")
	@app_commands.describe( member='Guild member to add to ticket.',
			      action = 'Action to perform with given member')
	@app_commands.choices(action=[
		app_commands.Choice(name="Rock", value="rock"),
		app_commands.Choice(name="Paper", value="paper")
    ])
	async def ticket_add_member_to_ticket(self, interaction: discord.Interaction, action: app_commands.Choice[str], member: discord.Member) -> None:
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
