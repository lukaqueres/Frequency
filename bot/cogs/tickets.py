import discord, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot, PIEmbed

class TicketLaunchView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Create ticket", style = discord.ButtonStyle.blurple, custom_id = "create_ticket_button")
	async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		#print("Button clicked")
		ticketPrefix = "ticket"
		ticket = utils.get(interaction.guild.text_channels, name=f"{ticketPrefix}-{interaction.user.name}-{interaction.user.discriminator}")
		if ticket is not None: return await interaction.response.send_message(f"There is a ticket opened already for you in {ticket.mention} channel. Write your message there.", ephemeral = True);
		else:
			pass
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
			interaction.user: discord.PermissionOverwrite(view_channel = True, send_messages = True, attach_files = True, embed_links = True),
			interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True)
		}

		channel = await interaction.guild.create_text_channel(name = f"{ticketPrefix}-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, category = interaction.channel.category, reason = f"As a ticket for user {interaction.user.name} #{interaction.user.discriminator}")
		ping = await channel.send(f">>> Channel especially for you, {interaction.user.mention}!");
		await ping.delete()
		title = f"Ticket with {interaction.user.name}"
		description = "Here you can talk to staff without disturbing"
		embed = PIEmbed(title = title, description = description)
		embed.timestamp = None
		await channel.send(embed = embed, view = TicketManageView());
		await interaction.response.send_message(content = f">>> Your ticket's channel has been created here: {channel.mention}", ephemeral = True)
		#except Exception as error:
		#	traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
class TicketCloseConfirmView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red, custom_id = "confirm_close_ticket_button")
	async def confirm_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		try: await interaction.channel.delete()
		except Exception as error: await interaction.response.send_message("Ticket closure failed, please check bot permissions", ephemeral = True)
		
	@discord.ui.button(label = "Abort", style = discord.ButtonStyle.grey, custom_id = "abort_ticket_closure_button")
	async def abort_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		await interaction.response.send_message("Ticket closure aborted. Disaffirming all actions.", ephemeral = True)

class TicketManageView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Close ticket", style = discord.ButtonStyle.red, custom_id = "close_ticket_button")
	async def close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		title = "Confirm ticket's closure"
		description = "After confirmation ticket will be closed with channel removed"
		embed = PIEmbed(title = title, description = description, color=discord.Colour.blurple())
		embed.timestamp = None
		await interaction.channel.send(embed = embed, view = TicketCloseConfirmView(), ephemeral = True)
		
		
class Tickets(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
	
	ticket = app_commands.Group(name="ticket", description="Tickets for guild users and admin contact.")
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="setup", description="Send embed with button allowing ticket creation.")
	async def tickets_set_ticket_creation_channel(self, interaction: discord.Interaction) -> None:
		title = "Use button below to create a ticket"
		description = "Clicking button will create channel with you and guild staff for conversation"
		embed = PIEmbed(title = title, description = description, color=discord.Colour.blurple())
		eembed.timestamp = None
		await interaction.channel.send(embed = embed, view = TicketLaunchView())
		await interaction.response.send_message(">>> Setup completed. You can disable/enable tickets by using `/ticket toggle`", ephemeral = True)
		
	
	@cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="toggle", description="Toggle creation of new tickets, can be enabled/disabled.")
	async def tickets_enable_or_disable(self, interaction: discord.Interaction) -> None:
		pass;
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="create", description="Create new ticket with guild contact team.")
	@app_commands.describe( member='Create ticket with member assigned. Guild staff only.' )
	async def ticket_create(self, interaction: discord.Interaction, member: Optional[discord.Member] = None) -> None:
		pass;
	
	@cooldown(1, 60, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="delete", description="Delete current ticket.")
	async def ticket_delete(self, interaction: discord.Interaction) -> None:
		pass;
	
	@cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="add_member", description="Add member to current ticket.")
	@app_commands.describe( member='Guild member to add to ticket.' )
	async def ticket_add_member_to_ticket(self, interaction: discord.Interaction, member: discord.Member) -> None:
		pass;
	
	@cooldown(1, 10, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="remove_member", description="Remove member from ticket.")
	@app_commands.describe( member='Guild member to remove from ticket.' )
	async def ticket_remove_member_from_ticket(self, interaction: discord.Interaction, member: discord.Member) -> None:
		pass;

async def setup(client: PIBot) -> None:
	await client.add_cog(Tickets(client))
