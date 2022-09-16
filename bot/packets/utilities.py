import discord
from typing import Optional

from discord import app_commands
from discord.ext import commands

from packets.discord import PIBot 

class Checks:
	def __init__(self, client: PIBot) -> None:
		self.client = client

	def __has_permission(self, permission):
		
	def has_privileges(self, **perms) -> commands.check: 
		if ctx:
			async def predicate(ctx):
				# Add the perms to a variable, you can format this any way you'd want
				ctx.command.required_perms = [p.replace('_', ' ').title() for p in perms.keys()]
				# Just use the normal check
				return await commands.has_permissions(**perms).predicate(ctx)
		else:
			async def predicate(ctx):
				# Add the perms to a variable, you can format this any way you'd want
				interaction.command.required_perms = [p.replace('_', ' ').title() for p in perms.keys()]
				# Just use the normal check
				return await commands.has_permissions(**perms).predicate(ctx)
			
		return commands.check(predicate)
			   
	def is_admin(self):
		def predicate(interaction: discord.Interaction = Null, ctx: commands.Context = Null):
			if ctx:
				return ctx.message.author.guild_permissions.administrator
			else:
				return interaction.user.guild_permissions.administrator
		return commands.check(predicate)
	
class CheckCooldown(Checks):
	def __init__(self, client: PIBot, check) -> None:
		super().__init__(client)
		self.cooldown = self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.guild)
		
	def update(self):
		retry = self.cooldown.get_bucket(interaction).update_rate_limit();
		if retry:
			return False;
		return True
