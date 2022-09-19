import discord, traceback, sys

from discord.ext import commands
from discord import app_commands

from packets.discord import PIBot
from packets.error import *

class Errors(commands.Cog, name="errors"):
	"""Errors handler."""
	def __init__(self, client: PIBot) -> None:
		self.client = client
		client.tree.error(coro = self.__dispatch_to_app_command_handler)

		self.default_error_message = ">>> There was an error while executing command."

	"""def help_custom(self):
		emoji = "<a:crossmark:842800737221607474>"
		label = "Error"
		description = "A custom errors handler. Nothing to see here."
		return emoji, label, description"""

	def trace_error(self, level: str, error: Exception):
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
		#self.bot.logger.name = f"discord.{level}"
		#self.bot.logger.error(msg=type(error).__name__, exc_info=error)
		
		raise error

	async def __reply_to_interaction(self, interaction: discord.Interaction, contnet:str):	
		try:
			await interaction.response.send_message(content=content, ephemeral=True)
			return True
		except discord.errors.InteractionResponded:
			interaction.edit_original_response(content = content)
			return True
		return False
		
	async def __reply_to_ctx(self, ctx: commands.Context, content:str):	
		ctx.send(content)
	
	async def __dispatch_to_app_command_handler(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		self.client.dispatch("app_command_error", interaction, error)

	async def __respond_to_interaction(self, interaction: discord.Interaction) -> bool:
		try:
			await interaction.response.send_message(content=self.default_error_message, ephemeral=True)
			return True
		except discord.errors.InteractionResponded:
			return False

	@commands.Cog.listener("on_error")
	async def get_error(self, event, *args, **kwargs):
		"""Error handler"""
		print(f"! Unexpected Internal Error: (event) {event}, (args) {args}, (kwargs) {kwargs}.")

	@commands.Cog.listener("on_command_error")
	async def get_command_error(self, ctx: commands.Context, error: commands.CommandError):
		"""Command Error handler
		doc: https://discordpy.readthedocs.io/en/master/ext/commands/api.html#exception-hierarchy
		"""
		try:
			#if ctx.interaction: # HybridCommand Support
			#	await self.__respond_to_interaction(ctx.interaction)
			#	edit = ctx.interaction.edit_original_message
			#	if isinstance(error, commands.HybridCommandError):
			#		error = error.original # Access to the original error
			#else:
			#	discord_message = await ctx.send(self.default_error_message)
			#	edit = discord_message.edit

			raise error

		# ConversionError
		except commands.ConversionError as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> {d_error}")
		# UserInputError
		except commands.MissingRequiredArgument as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> Something is missing. `{ctx.clean_prefix}{ctx.command.name} <{'> <'.join(ctx.command.clean_params)}>`")
		# UserInputError -> BadArgument
		except commands.MemberNotFound or commands.UserNotFound as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> Member `{str(d_error).split(' ')[1]}` not found ! Don't hesitate to ping the requested member.")
		# UserInputError -> BadUnionArgument | BadLiteralArgument | ArgumentParsingError
		except commands.BadArgument or commands.BadUnionArgument or commands.BadLiteralArgument or commands.ArgumentParsingError as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> {d_error}")
		# CommandNotFound
		except commands.CommandNotFound as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> Command `{str(d_error).split(' ')[1]}` not found!")
		# CheckFailure
		except commands.PrivateMessageOnly:
			await self.__reply_to_ctx(ctx = ctx, content = ">>> This command canno't be used in a guild, try in direct message.")
		except commands.NoPrivateMessage:
			await self.__reply_to_ctx(ctx = ctx, content = ">>> This is not working as excpected.")
		except commands.NotOwner:
			await self.__reply_to_ctx(ctx = ctx, content = ">>> You must own this bot to run this command.")
		except commands.MissingPermissions as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> You are lacking `{'` `'.join(d_error.missing_permissions)}` permission{ 's' if len(d_error.missing_permissions) > 0 else ''} to run this command.")
		except commands.BotMissingPermissions as d_error:
			if not "send_messages" in d_error.missing_permissions:
				await self.__reply_to_ctx(ctx = ctx, content = f">>> This command require bot to have `{'` `'.join(d_error.missing_permissions)}` permissions.")
		except commands.CheckAnyFailure or commands.MissingRole or commands.BotMissingRole or commands.MissingAnyRole or commands.BotMissingAnyRole as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> {d_error}")
		except commands.NSFWChannelRequired:
			await self.__reply_to_ctx(ctx = ctx, content = ">>> This command can be only used in NSFW channel.")
		# DisabledCommand
		except commands.DisabledCommand:
			await self.__reply_to_ctx(ctx = ctx, content = ">>> Sorry, this command is currently disabled.")
		# CommandInvokeError
		except commands.CommandInvokeError as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> {d_error.original}")
		# CommandOnCooldown
		except commands.CommandOnCooldown as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> Command is on cooldown, please wait `{str(d_error).split(' ')[7]}` !")
		# MaxConcurrencyReached
		except commands.MaxConcurrencyReached as d_error:
			await self.__reply_to_ctx(ctx = ctx, content = f">>> Max concurrency reached. Maximum number of concurrent invokers allowed: `{d_error.number}`, per `{d_error.per}`.")
		# HybridCommandError
		except commands.HybridCommandError as d_error:
			await self.get_app_command_error(ctx.interaction, error)
		# - CUSTOM ERRORS -
		#except CommandOnCooldown as d_error:
		#	return await d_error.interaction.response.send_message(content=f">>> Command `{d_error.command}` is now on cooldown, try again in `{round(d_error.retry, 1)}s`.", ephemeral=True)
		except Exception as e:
			await self.__reply_to_ctx( ctx = ctx, content = self.default_error_message )
			print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
			traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			self.trace_error("get_command_error", e)

	@commands.Cog.listener("on_app_command_error")
	async def get_app_command_error(self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
		"""App command Error Handler
		doc: https://discordpy.readthedocs.io/en/master/interactions/api.html#exception-hierarchy
		"""
		try:
			#await self.__respond_to_interaction(interaction)
			#edit = interaction.edit_original_response #interaction.edit_original_message

			raise error
		except app_commands.CommandInvokeError as d_error:
			if isinstance(d_error.original, discord.errors.InteractionResponded):
				await self.__reply_to_interaction( interaction = interaction, content = f">>> {d_error.original}")
			elif isinstance(d_error.original, discord.errors.Forbidden):
				await self.__reply_to_interaction( interaction = interaction, content = f">>> `{type(d_error.original).__name__}` : {d_error.original.text}")
				#await edit(content=f"`{type(d_error.original).__name__}` : {d_error.original.text}")
			else:
				self.trace_error("get_view_error", d_error)
				#await self.__reply_to_interaction( interaction = interaction, content = f"`{type(d_error.original).__name__}` : {d_error.original}")
		except app_commands.CheckFailure as d_error:
			if isinstance(d_error, app_commands.errors.CommandOnCooldown):
				await self.__reply_to_interaction( interaction = interaction, content = f">>> Command is on cooldown, wait `{str(d_error).split(' ')[7]}` !")
			else:
				await self.__reply_to_interaction( interaction = interaction, content = f">>> `{type(d_error).__name__}` : {d_error}")
		except app_commands.CommandNotFound:
			await self.__reply_to_interaction( interaction = interaction, content = f">>> Command was not found.. Seems to be a discord bug, probably due to desynchronization.\nMaybe there is multiple commands with the same name, you should try the other one.")
		except Exception as e: 
			"""
			Caught here:
			app_commands.TransformerError
			app_commands.CommandLimitReached
			app_commands.CommandAlreadyRegistered
			app_commands.CommandSignatureMismatch
			"""
			#print('Ignoring exception in command {}:'.format(interaction.command), file=sys.stderr)
			#traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
			await self.__reply_to_interaction( interaction = interaction, content = self.default_error_message )
			self.trace_error("get_app_command_error", e)

	@commands.Cog.listener("on_view_error")
	async def get_view_error(self, interaction: discord.Interaction, error: Exception, item: any):
		"""View Error Handler"""
		try:
			raise error
		except discord.errors.Forbidden:
			pass
		except Exception as e:
			self.trace_error("get_view_error", e)

	@commands.Cog.listener("on_modal_error")
	async def get_modal_error(self, interaction: discord.Interaction, error: Exception):
		"""Modal Error Handler"""
		try:
			raise error
		except discord.errors.Forbidden:
			pass
		except Exception as e:
			self.trace_error("get_modal_error", e)

async def setup(client: PIBot):
	await client.add_cog(Errors(client))
