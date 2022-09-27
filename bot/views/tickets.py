import discord, datetime, os, traceback, sys

from discord.ext import commands
from discord import app_commands, utils
from discord.app_commands.checks import has_permissions, cooldown

from typing import Optional

from packets.discord import PIBot, PIEmbed

from views.PIView import PIView
	
class TicketConsoleView(PIView):
	def __init__(self) -> None:
		super().__init__(timeout = 600.0)
		
	@discord.ui.button(label = "Send ticket embed", style = discord.ButtonStyle.blurple, custom_id = "send_ticket_embed_button")
	async def send_ticket_embed_button(self, interaction: discord.Interaction, button: discord.ui.button):
		from cogs.tickets import Ticket
		try:
			ticket = Ticket( interaction = interaction, user = interaction.user)
			await ticket.create()
			#await self.functions.create_ticket(interaction = interaction, for_member = interaction.user)
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
	@discord.ui.button(label = "Add member", style = discord.ButtonStyle.blurple, custom_id = "add_member_embed_button")
	async def add_member_to_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		pass
	
class TicketLaunchView(PIView):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Create ticket", style = discord.ButtonStyle.blurple, custom_id = "create_ticket_button")
	async def create_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		from cogs.tickets import Ticket
		try:
			ticket = Ticket( interaction = interaction, user = interaction.user)
			await ticket.create()
			#await self.functions.create_ticket(interaction = interaction, for_member = interaction.user)
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
class TicketCloseConfirmView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = 300.0)

	@discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red)
	async def confirm_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		await interaction.response.send_message("Closing current ticket...", ephemeral = True)
		try: await interaction.channel.delete(reason = f"Closed ticket for user {interaction.user.name}")
		except Exception as error: return await interaction.edit_original_response(content = "Ticket closure failed, please check bot permissions", ephemeral = True)
		
	@discord.ui.button(label = "Abort", style = discord.ButtonStyle.grey)
	async def abort_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		for child in button.view.children:
			child.disable = True
		button.view.stop()
		await interaction.response.send_message("Ticket closure aborted. Disaffirming all actions.", ephemeral = True)
		
	@discord.ui.TextInput(label = "Reason", style=discord.TextStyle.short, custom_id = "ticket_reason_of_close_input", placeholder="Input reason for ticket close", default=None, required=False, min_length=0, max_length=100, row=2)
	async def add_reason_of_close_to_ticket(self, interaction, TextInput: discord.ui.TextInput):
		await interaction.response.send_message(TextInput.value, ephemeral = True)
		

class TicketManageView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Close ticket", style = discord.ButtonStyle.red, custom_id = "close_ticket_button")
	async def close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		from cogs.tickets import Ticket
		try:
			ticket = Ticket(interaction = interaction)
			await ticket.confirm_close()
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
	@discord.ui.button(label = "Tally", style = discord.ButtonStyle.blurple, custom_id = "generate_ticket_tally_button")
	async def generate_ticket_tally_button(self, interaction: discord.Interaction, button: discord.ui.button):
		try:
			await interaction.response.defer()
			if not os.path.exists("tallies/"):
    				os.makedirs("tallies/")
			
			if os.path.exists(f"tallies/{interaction.channel.id}.md"):
				return await interaction.followup.send(">>> Tally for this ticket is already being inscribed!", ephemeral = True)
			with open(f"tallies/{interaction.channel.id}.md", 'a') as f:
				f.write(f"# Tally for ticket in channel {interaction.channel.name}:\n\n")
				async for message in interaction.channel.history(limit = 500, oldest_first = True):
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
				await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
				os.remove(f"tallies/{interaction.channel.id}.md")
		except Exception as error:
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		
