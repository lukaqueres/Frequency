import discord, datetime, os

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
		await interaction.response.send_message("Creating ticket...", ephemeral = True)
		ticketPrefix = "ticket"
		ticket = utils.get(interaction.guild.text_channels, name=f"{ticketPrefix}-{interaction.user.name}-{interaction.user.discriminator}")
		if ticket is not None: return await interaction.edit_original_response(content = f"There is a ticket opened already for you in {ticket.mention} channel. Write your message there.", ephemeral = True);
		else:
			pass
		moderatorId = 1020060418871414824
		ticketModerator = interaction.guild.get_role(moderatorId)
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(view_channel = False),
			interaction.user: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True),
			interaction.guild.me: discord.PermissionOverwrite(view_channel = True, send_messages = True, read_message_history = True),
			ticketModerator: discord.PermissionOverwrite(view_channel = True, read_message_history = True, send_messages = True, attach_files = True, embed_links = True)
		}
		try: channel = await interaction.guild.create_text_channel(name = f"{ticketPrefix}-{interaction.user.name}-{interaction.user.discriminator}", overwrites = overwrites, category = interaction.channel.category, reason = f"As a ticket for user {interaction.user.name} #{interaction.user.discriminator}")
		except: return await interaction.edit_original_response(content = "Ticket creation failed, please check bot permissions", ephemeral = True)
		ping = await channel.send(f">>> Ticket with: {interaction.user.mention}, {ticketModerator.mention}.");
		await ping.delete()
		title = f"Ticket with {interaction.user.name}"
		description = "Here you can talk to staff without disturbing"
		embed = PIEmbed(title = title, description = description)
		embed.timestamp = None
		await channel.send(embed = embed, view = TicketManageView());
		await interaction.edit_original_response(content = f">>> Your ticket's channel has been created here: {channel.mention}")
		#except Exception as error:
		#	traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			
class TicketCloseConfirmView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = 300.0)

	@discord.ui.button(label = "Confirm", style = discord.ButtonStyle.red)
	async def confirm_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		await interaction.response.send_message("Closing current ticket...", ephemeral = True)
		try: await interaction.channel.delete()
		except Exception as error: return await interaction.edit_original_response(content = "Ticket closure failed, please check bot permissions", ephemeral = True)
		
	@discord.ui.button(label = "Abort", style = discord.ButtonStyle.grey)
	async def abort_close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		for child in button.view.children:
			child.disable = True
		button.view.stop()
		await interaction.response.send_message("Ticket closure aborted. Disaffirming all actions.", ephemeral = True)

class TicketManageView(discord.ui.View):
	def __init__(self) -> None:
		super().__init__(timeout = None)

	@discord.ui.button(label = "Close ticket", style = discord.ButtonStyle.red, custom_id = "close_ticket_button")
	async def close_ticket_button(self, interaction: discord.Interaction, button: discord.ui.button):
		title = "Confirm ticket's closure"
		description = "After confirmation ticket will be closed with channel removed"
		embed = PIEmbed(title = title, description = description)
		embed.timestamp = None
		await interaction.response.send_message(embed = embed, view = TicketCloseConfirmView(), ephemeral = True)
		
	@discord.ui.button(label = "Tally", style = discord.ButtonStyle.blurple, custom_id = "generate_ticket_tally_button")
	async def generate_ticket_tally_button(self, interaction: discord.Interaction, button: discord.ui.button):
		await interaction.response.defer()
		print("file checking")
		if os.path.exists(f"tallies/{interaction.channel.id}.md"):
			return await interaction.followup.send(">>> Tally for this ticket is already being inscribed!", ephemeral = True)
		print("file creating")
		with open(f"tallies/{interaction.channel.id}.md", 'a') as f:
			f.write(f"# Tally for ticket in channel {interaction.channel.name}:\n\n")
			async for message in interaction.channel.history(limit = 500, oldest_first = True):
				created = datetime.strftime(message.created_at, "%d.%m.%Y at %H:%M:%S")
				if message.edited_at:
					edited = datetime.strftime(message.edited_at, "%d.%m.%Y at %H:%M:%S")
					f.write(f"{message.author} on {created}: {message.clean_content} ( Edited at {edited} )\n")
				else:
					f.write(f"{message.author} on {created}: {message.clean_content}\n")
			generated = datetime.now().strftime("%d.%m.%Y at %H:%M:%S")
			f.write(f"## Tally inscribed by {client.user.name} for {interaction.user.name}\nOn {generated}, Time Zone: UTC")
		print("file created")
		with open(f"tallies/{interaction.channel.id}.md", 'rb') as f:
			await interaction.followup.send(file = discord.File(f, f"{interaction.channel.name}.md"))
			os.remove(f"tallies/{interaction.channel.id}.md")
		
