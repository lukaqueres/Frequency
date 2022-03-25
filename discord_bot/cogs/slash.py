import discord, json, io, os, typing, requests, random, asyncio
from discord import member, DMChannel, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option

from datetime import datetime, date, timedelta
from functions import get_prefix, get_time, get_guilds_ids

intents = discord.Intents.all()
client = commands.Bot(command_prefix = get_prefix, Intents=intents)

#slash = SlashCommand(client, sync_commands=True)

guild_ids = get_guilds_ids()

async def commands_modules():
	return ["test","tust","tast","tist"]

def convert_timedelta(duration): # Function to convert the time
    days, seconds = duration.days, duration.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = (seconds % 60)
    return days, hours, minutes, seconds

class Slash(Cog):
	def __init__(self, client: Bot):
		self.client = client
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Slash commands module loaded')
    
	@cog_ext.cog_slash(name="clear", 
	                   description="Delets messages by number or filter", 
	                   guild_ids=guild_ids,
	                   options=[
				   create_option(
                                	name = "amount",
                                	description = "Set number of messages to delete / filter of",
                                	option_type = 4,
                                	required = False
                               	   ),
				   create_option(
                                	name = "days",
                                	description = "Restrict by message age",
                                	option_type = 4,
                                	required = False
                               	   ),
				   create_option(
                                	name = "member",
                                	description = "Restrict by message author",
                                	option_type = 6,
                                	required = False
                               	   )])
	@commands.has_permissions(manage_messages=True)
	async def _clear(self, ctx: SlashContext, amount: int = 200, member = None, days = 62): 
		if amount <= 0 or amount > 200:
			return await ctx.send(">>> Invalid number given. Number must fit between 1 and 200", hidden=True)
		if days <= 0 or days > 62:
			return await ctx.send(">>> Invalid days count given. Messages to delete can be max 62 days old", hidden=True)
		#channel = ctx.channel
		#if member:
			#await ctx.channel.purge(limit=amount, check=lambda message: message.author == member)
		#else:
			#await ctx.channel.purge(limit = amount)
		deleted_messages = 0
		after_date = datetime.utcnow()-timedelta(days=days)
		total_messages_count = 0
		async for message in ctx.channel.history(limit=amount, after=after_date):
			total_messages_count += 1
			if member and message.author == member:
				deleted_messages += 1
				await message.delete()
			elif member and message.author != member:
				continue
			else:
				deleted_messages += 1
				await message.delete()
		
		if deleted_messages > 0:
			embed = Embed(title=f"Deleted {deleted_messages} messages" if deleted_messages > 1 else "Deleted 1 message",
				colour = 0x206694,
				description = f"Out of {total_messages_count} messages in time range and limit"
				)
		
			#embed.add_field( name=f"Deleted {deleted_messages} messages", value=f"Out of {total_messages_count} messages in time range and limit", inline=False),
		elif total_messages_count == 0:
			embed = Embed(title=f"No messages deleted",
				colour = 0x206694,
				description = f"There was no messages that matched provided deletion criteria"
				)
		else:
			embed = Embed(title=f"No messages deleted",
				colour = 0x206694,
				description = f"None of { total_messages_count } messages matched provided deletion criteria"
				)
			#embed.add_field( name=f"No messages deleted", value=f"None of { total_messages_count } messages matched provided deletion criteria", inline=False),
		await ctx.send(embed = embed , hidden=True)
	
	@_clear.error
	async def _clear_error(self, ctx: SlashContext, error):
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!", hidden=True)
		else: 
			print(error)
			await ctx.channel.send("There was an error with executing command!", hidden=True)

        
	@cog_ext.cog_slash(name="help", 
				guild_ids=guild_ids, 
				description="Provides information about bot itself or specific commands",
                       options=[create_option(
                                   name = "target",
                                   description = "What command or module do you want learn more about?",
                                   option_type = 3,
                                   required = False,
			           choices = [
					   create_choice(name = 'Music', value='music'), create_choice(name = 'clear', value='clear'), create_choice(name = 'More', value='more')
				   ]
                                )])
	async def _help(self, ctx: SlashContext, target = None):
		if not ctx.author.guild_permissions.manage_messages:
			return await ctx.send(">>> You can't use this!", hidden=True)
		embed = Embed(title="Embed Test")
		await ctx.send(embed=embed, hidden=True)

		
	@cog_ext.cog_slash(name="user", 
	                   description="Provides various options for user management", 
	                   guild_ids=guild_ids,
	                   options=[
				   create_option(
                                   	name = "member",
                                   	description = "Choose member action will take affect on.",
                                   	option_type = 6,
                                   	required = True,
                                   ),
			   	   create_option(
                                   	name = "action",
                                   	description = "Choose action.",
                                   	option_type = 3,
                                   	required = True,
					choices = [
						create_choice(name = 'Information', value='information'), 
						create_choice(name = 'Ban', value='ban')
				   	]
                                  ),
			   	  create_option(
                                   	name = "reason",
                                   	description = "Input reason of actions that by default requires it.",
                                   	option_type = 3,
                                   	required = False,
                                   ),
			   	  create_option(
                                   	name = "timerange",
                                   	description = "Input time span for actions that requires it.",
                                   	option_type = 4,
                                   	required = False,
                                   )])
	async def _user(self, ctx: SlashContext, member = "autor", action = None, reason = None, timerange = None): 
		user = member
		rolelist = [r.name for r in user.roles if r != ctx.guild.default_role]
		roles = " | ".join(reversed(rolelist))
		account_created = user.created_at.strftime("%d/%m/%Y %H:%M:%S")
		guild_join = user.joined_at.strftime("%d/%m/%Y %H:%M:%S")
		if action == 'information':
			if timerange:
				if (timerange > 21 or timerange < 1):
					return await ctx.send( "Invalid time range ammount given. Must Oscilate between 1 and 21 days." , hidden=True)
			await ctx.defer()
			if timerange:
				after_date = datetime.utcnow()-timedelta(days=timerange)
			today = datetime.today()
			account_created_date = user.created_at
			guild_join_date = user.joined_at
			now = datetime.utcnow() # UTC time, can be changed

			days_til_join = now - guild_join_date # Do some maths
			days_til_create = now - account_created_date # Do some maths
			jdays, jhours, jminutes, jseconds = convert_timedelta(days_til_join) # Build in a converter
			cdays, chours, cminutes, cseconds = convert_timedelta(days_til_create) # Build in a converter
			embed = Embed(title="User information",
				colour = user.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=user.avatar_url)
      	
			embed.add_field( name=chr(173), value=f"**User**: {str(user)}\n**User ID**: {user.id}", inline=True),
			embed.add_field( name=chr(173), value=f"**Created**: {account_created}, **{cdays}** days ago \n**Joined**: {guild_join}, **{jdays}** days ago", inline=True),
			#embed.add_field(name = chr(173), value = chr(173), inline=False)
			embed.add_field( name="All roles:", value=roles if roles else "No roles", inline=False), #if roles else "No roles"
			embed.add_field(name = chr(173), value = f"**Status**: {str(user.status).title()}\n**Activity**: {str(user.activity.type).split('.')[-1].title() if user.activity else 'N/A'} {user.activity.name if user.activity else ''}\n**Bot**: {'NO' if not user.bot else 'YES'}", inline=True),
			embed.add_field( name= chr(173), value=f"**Top role**: {user.top_role.name}\n**Number of roles**: {len(rolelist)}\n**Nitro**: { 'Yes' if bool(user.premium_since) else 'No'}", inline=True),
			guild_channels = ctx.guild.text_channels
			if timerange != None:
				messages_per_channel = {}
				for channel in guild_channels:
					total_messages_count = 0
					messages_count = 0
					async for message in channel.history(limit=500, after=after_date):
						if message.author == member:
							messages_count += 1
					if messages_count == 0:
						pass
					else:
						messages_per_channel[messages_count] = channel.name
				keys = list(messages_per_channel.keys())
				keys.sort()
				keys.reverse()
				displayed = 0
				max_display = 5
				message = "\n"
				for key in keys:
					if displayed == max_display:
						break
					displayed += 1
					message += f"**{messages_per_channel[key]}** : **{key}**\n"
				embed.add_field( name=f"Last {timerange} days of user message activity:", value=message, inline=False),
				#embed.add_field( name= f"Messages count in channel: {messages_per_channel[key]}", value=key, inline=True),
			embed.set_footer(text="Provided by Wild West Post Office")
			await ctx.send(embed=embed)
		if action == 'ban':
			today = datetime.today()
			account_created_date = user.created_at
			guild_join_date = user.joined_at
			now = datetime.utcnow() # UTC time, can be changed

			days_til_join = now - guild_join_date # Do some maths
			days_til_create = now - account_created_date # Do some maths
			jdays, jhours, jminutes, jseconds = convert_timedelta(days_til_join) # Build in a converter
			cdays, chours, cminutes, cseconds = convert_timedelta(days_til_create) # Build in a converter
			account_created = str(account_created)
			guild_join = str(guild_join)
			account_created = account_created[:-4]
			guild_join = guild_join[:-4]
			embed = Embed(title="User banned",
				colour = user.colour,
				#timestamp=get_time()
				)
			embed.set_thumbnail(url=user.avatar_url)
      	
			embed.add_field( name=chr(173), value=f"**User**: {str(user)}\n**User ID**: {user.id}", inline=True),
			embed.add_field( name=chr(173), value=f"**Created**: {account_created}, **{cdays}** days ago \n**Joined**: {guild_join}, **{jdays}** days ago", inline=True),
			embed.add_field( name=chr(173), value=f"**Reason**: {reason if reason else 'No reason provided'}", inline=False),
			
			await ctx.send(embed=embed)
		
def setup(client: client):
	client.add_cog(Slash(client))

    
    
    
