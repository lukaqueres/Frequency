import discord

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot

class Tickets(commands.Cog):
	def __init__(self, client: PIBot) -> None:
		super().__init__()
		self.client = client
	
	ticket = app_commands.Group(name="ticket", description="Tickets for guild users and admin contact.")
	
	@cooldown(1, 600, key=lambda i: (i.guild_id, i.user.id))
	@ticket.command(name="set_channel", description="Set channel for tickets creation button.")
	@app_commands.describe( channel='Choose channel to send embed about tickets. Leave empty for command channel.' )
	async def tickets_set_button_channel(self, interaction: discord.Interaction, channel: Optional[discord.channel.TextChannel] = None) -> None:
		pass;
	
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

class TicketView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)
		
	@discord.ui.button(label = "create_ticket", style = discord.ButtonStyle.blurple, custom_id = "create_ticket_button")
	async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		ticketPrefix = "ticket"
		ticket = utils.get(interaction.guild.text_channels, name=f"{ticketPrefix}-{interaction.user.name}-{interaction.user.discriminator}")
		if ticket is not None:
			await interaction.response.send_message(f"There is a ticket opened already for you in {ticket.mention} channel. Write your message there.")

async def setup(client: PIBot) -> None:
	await client.add_cog(Tickets(client))
