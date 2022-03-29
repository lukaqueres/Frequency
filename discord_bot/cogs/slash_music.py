import discord, json, io, os, typing, requests, random, asyncio
from discord import member, DMChannel, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import has_permissions, MissingPermissions

#from discord_components import DiscordComponents, ComponentsBot, Button, SelectOption, Select

#from discord import Button, ButtonStyle

from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

from datetime import datetime, date, timedelta
from functions import get_prefix, get_time, get_guilds_ids

import itertools
import sys
import traceback
import psycopg2
import re
import functools
import math
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio, Embed
from datetime import datetime, date, timedelta


intents = discord.Intents.all()
client, bot = (commands.Bot(command_prefix = get_prefix, Intents=intents),)*2

#slash = SlashCommand(client, sync_commands=True)

guild_ids = get_guilds_ids()

ytdlopts = {
	'format': 'bestaudio/best',
	'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'yesplaylist': True, #True
	'playlistrandom' : True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0',  # ipv6 addresses cause issues sometimes
	'force-ipv4': True
}

ffmpegopts = {
	#'before_options': '-nostdin',
	'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
	'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)
"""
class MusicButtons(discord.ui.View):
	def __init__(self, *, timeout=180):
		super().__init__(timeout=timeout)
	@discord.ui.button(label="Blurple Button",style=discord.ButtonStyle.blurple,emoji="🎶") # or .primary
	async def blurple_button(self,button:discord.ui.Button,interaction:discord.Interaction):
		button.disabled=True
		await interaction.response.edit_message(view=self)
	@discord.ui.button(label="Gray Button",style=discord.ButtonStyle.gray,emoji="🎵") # or .secondary/.grey
	async def gray_button(self,button:discord.ui.Button,interaction:discord.Interaction):
		button.disabled=True
		await interaction.response.edit_message(view=self)
	@discord.ui.button(label="Green Button",style=discord.ButtonStyle.green,emoji="⏹️") # or .success
	async def green_button(self,button:discord.ui.Button,interaction:discord.Interaction):
		button.disabled=True
		await interaction.response.edit_message(view=self)
	@discord.ui.button(label="Red Button",style=discord.ButtonStyle.red,emoji="⏯️") # or .danger
	async def red_button(self,button:discord.ui.Button,interaction:discord.Interaction):
		button.disabled=True
		await interaction.response.edit_message(view=self)
	@discord.ui.button(label="Red Button",style=discord.ButtonStyle.red,emoji="⏭️") # or .danger
	async def red_button(self,button:discord.ui.Button,interaction:discord.Interaction):
		button.disabled=True
		await interaction.response.edit_message(view=self)
"""
class VoiceConnectionError(commands.CommandError):
	"""Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
	"""Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

	def __init__(self, source, *, data, requester):
		super().__init__(source)
		self.requester = requester
		date = data.get('upload_date') 

		self.title = data.get('title')
		self.web_url = data.get('webpage_url')
		self.thumbnail = data.get('thumbnail')
		self.description = data.get('description')
		if len(self.description) > 800:
			self.description = self.description[:800] + '...'
		self.duration = self.parse_duration(int(data.get('duration')))
		self.tags = data.get('tags')
		self.url = data.get('webpage_url')
		self.views = data.get('view_count')
		self.likes = data.get('like_count')
		self.uploader = data.get('uploader')
		self.upload_date = date[6:8] + '.' + date[4:6] + '.' + date[0:4]

		# YTDL info dicts (data) have other useful information you might want
		# https://github.com/rg3/youtube-dl/blob/master/README.md

	@staticmethod
	def parse_duration(duration: int):
		minutes, seconds = divmod(duration, 60)
		hours, minutes = divmod(minutes, 60)
		days, hours = divmod(hours, 24)

		duration = []
		if days > 0:
			duration.append('{} days'.format(days))
		if hours > 0:
			duration.append('{} hours'.format(hours))
		if minutes > 0:
			duration.append('{} minutes'.format(minutes))
		if seconds > 0:
			duration.append('{} seconds'.format(seconds))

		return ', '.join(duration)
	
	def __getitem__(self, item: str):
		"""Allows us to access attributes similar to a dict.
		This is only useful when you are NOT downloading.
		"""
		return self.__getattribute__(item)

	@classmethod
	async def create_source(cls, ctx, search: str, *, loop, download=False):
		loop = loop or asyncio.get_event_loop()

		to_run = partial(ytdl.extract_info, url=search, download=download)
		data = await loop.run_in_executor(None, to_run)
		#print(f'To_run: {to_run}')
		#print(f'Data: {data}' )
		if not data:
			return "type_playlist"
		if 'entries' in data:
			# take first item from a playlist
			id_list = []
			#data = []
			#iteration = 0
			for item in data['entries']:
				id_list.append(item['id'])
				if len(id_list) > 1:
					return "type_playlist" # return playlist type
			#print(f"Liczba id: {len(id_list)}")
			#print(f"Lista id: {id_list}")
			data = data['entries'][0]
		duration = int(data['duration'])
		duration = YTDLSource.parse_duration(duration)
		
		embed = discord.Embed( 
			title="Added to queue",
			description="You can always check queue with *queue* command",
			color= ctx.message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.add_field(name= "Title:", value=data["title"], inline=True),
		embed.add_field(name= "Duration:", value=duration, inline=True),
		embed.add_field(name= "Url:", value=data['webpage_url'], inline=False),
		embed.add_field(name= "Requested by:", value=ctx.author, inline=True),
		await ctx.send(embed = embed, delete_after=15)

		if download:
			source = ytdl.prepare_filename(data)
		else:
			return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'], 'duration' : int(data.get('duration')), 'thumbnail' : data.get('thumbnail')}
		
		return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

	@classmethod
	async def add_to_queue(cls, ctx, directory, player):
		#player = Music.get_player(ctx = ctx)

		await player.queue.put(directory)
		data = directory
		"""embed = discord.Embed( 
			title="Added to queue",
			description="You can always check queue with *queue* command",
			color= ctx.message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 )
		)
		embed.add_field(name= "Title:", value=data["title"], inline=True),
		embed.add_field(name= "Requested by:", value=ctx.author, inline=True),
		await ctx.send(embed = embed, delete_after=15)"""

	@classmethod
	async def create_source_from_playlist(cls, ctx, search: str, *, loop, download=False, player):
		loop = loop or asyncio.get_event_loop()
		to_run = partial(ytdl.extract_info, url=search, download=download)
		data = await loop.run_in_executor(None, to_run)
		#print(f'To_run: {to_run}')
		#print(f'Data: {data}' )
		#if 'entries' in data:
		status = True
		list_title = data['title']
		#list_thumbnail = data.get('thumbnail')
		if status:
			# take first item from a playlist
			entries_list = []
			#data = []
			#iteration = 0
			for item in data['entries']:
				entries_list.append(item)
			for entry in entries_list:
				data = entry
				directory = {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'], 'duration' : int(data.get('duration')), 'thumbnail' : data.get('thumbnail')}
				await cls.add_to_queue(ctx, directory, player)

			#print(f"Lista entries: {entries_list}")
			#print(f"Liczba entries: {len(entries_list)}")
			total_duration = 0
			for _ in entries_list:
				total_duration = total_duration + int(_['duration'])
			total_duration = YTDLSource.parse_duration(total_duration)
			embed = discord.Embed( 
				title="Playlist songs added to queue",
				description="You can always check queue with *queue* command",
				color= ctx.message.author.colour,
				timestamp=datetime.utcnow() + timedelta( hours = 0 )
			)
			#embed.set_thumbnail(url= list_thumbnail)
			embed.add_field(name= 'Title:', value= list_title, inline=False),
			embed.add_field(name= chr(173), value=f"**Number of songs**: {len(entries_list)}\n**Total duration**: {total_duration}", inline=True),
			embed.add_field(name= "Requested by:", value=ctx.author, inline=True),
			await ctx.send(embed = embed, delete_after=15)
			return 0

			data = data['entries'][0]

		if download:
			source = ytdl.prepare_filename(data)
			return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)
		else:
			return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title'], 'duration' : int(data.get('duration')), 'thumbnail' : data.get('thumbnail')}
		
	@classmethod
	async def regather_stream(cls, data, *, loop):
		"""Used for preparing a stream, instead of downloading.
		Since Youtube Streaming links expire."""
		loop = loop or asyncio.get_event_loop()
		requester = data['requester']

		to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
		data = await loop.run_in_executor(None, to_run)

		return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
	"""A class which is assigned to each guild using the bot for Music.
	This class implements a queue and loop, which allows for different guilds to listen to different playlists
	simultaneously.
	When the bot disconnects from the Voice it's instance will be destroyed.
	"""

	__slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

	def __init__(self, ctx):
		self.bot = ctx.bot
		self._guild = ctx.guild
		self._channel = ctx.channel
		self._cog = ctx.cog

		self.queue = asyncio.Queue()
		self.next = asyncio.Event()

		self.np = None  # Now playing message
		self.volume = .5
		self.current = None

		ctx.bot.loop.create_task(self.player_loop())

	async def player_loop(self):
		"""Our main player loop."""
		await self.bot.wait_until_ready()

		while not self.bot.is_closed():
			self.next.clear()

			try:
				# Wait for the next song. If we timeout cancel the player and disconnect...
				async with timeout(300):  # 5 minutes...
					source = await self.queue.get()
			except asyncio.TimeoutError:
				return self.destroy(self._guild)

			if not isinstance(source, YTDLSource):
				# Source was probably a stream (not downloaded)
				# So we should regather to prevent stream expiration
				try:
					source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
				except Exception as e:
					await self._channel.send(f'There was an error processing your song.\n'
											f'```css\n[{e}]\n```')
					continue

			source.volume = self.volume
			self.current = source

			self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
			self.np = await self._channel.send(f'**Now Playing:** `{source.title}` requested by '
                                               f'`{source.requester}`')
			await self.next.wait()

			# Make sure the FFmpeg process is cleaned up.
			source.cleanup()
			self.current = None

			try:
				# We are no longer playing this song...
				await self.np.delete()
			except discord.HTTPException:
				pass

	def destroy(self, guild):
		"""Disconnect and cleanup the player."""
		return self.bot.loop.create_task(self._cog.cleanup(guild))

class Slash_music(Cog):
	"""Commands for playing music, and its managing"""
	__slots__ = ('bot', 'players')
	
	def __init__(self, client):
		self.bot = bot
		self.client = client
		self.players = {}
	
	async def cleanup(self, guild):
		try:
			await guild.voice_client.disconnect()
		except AttributeError:
			pass

		try:
			del self.players[guild.id]
		except KeyError:
			pass

	async def __local_check(self, ctx):
		"""A local check which applies to all commands in this cog."""
		if not ctx.guild:
			raise commands.NoPrivateMessage
		return True

	async def cog_command_error(self, ctx, error):
		"""A local error handler for all errors arising from commands in this cog."""
		if isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.send('This command can not be used in Private Messages.')
			except discord.HTTPException:
				pass
		elif isinstance(error, InvalidVoiceChannel):
			await ctx.send('Error connecting to Voice Channel. '
							'Please make sure you are in a valid channel or provide me with one')
		elif isinstance(error, youtube_dl.utils.RegexNotFoundError):
			await ctx.send('There was error while downloading song, you can try again.')
			print(error)

		print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
		traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

	def get_player(self, ctx):
		"""Retrieve the guild player, or generate one."""
		try:
			player = self.players[ctx.guild.id]
		except KeyError:
			player = MusicPlayer(ctx)
			self.players[ctx.guild.id] = player

		return player
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Slash music module loaded')
		
	#music = client.create_group("music", "Music related commands.")

	@cog_ext.cog_slash(name="connect", 
	                   description="Connect to voice channel", 
	                   guild_ids=guild_ids,
	                   #options=[
			#	   create_option(
                         #       	name = "channel",
                          #      	description = "Choose voice channel to connect, if not specified, bot will join current user channel",
                           #     	option_type = discord.VoiceChannel, #7
                            #    	required = False,
                             #  	   )]
			   )
	async def connect_(self, ctx): # , *, channel: discord.VoiceChannel=None
		"""Connect to voice.
		Parameters
		------------
		channel: discord.VoiceChannel [Optional]
			The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
			will be made.
		This command also handles moving the bot to different channels.
		"""
		channel = None
		if not channel:
			try:
				channel = ctx.author.voice.channel
			except AttributeError:
				raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')
				return await ctx.send( ">>> Error connecting voice channel. No channel to join.", hidden = True)

		vc = ctx.voice_client

		if vc:
			if vc.channel.id == channel.id:
				return
			try:
				await vc.move_to(channel)
			except asyncio.TimeoutError:
				raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
		else:
			try:
				await channel.connect()
			except asyncio.TimeoutError:
				raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

		await ctx.send(f'Connected to: **{channel}**', delete_after=20)

	
	@cog_ext.cog_slash(name="play", 
	                   description="Play music from url or key words", 
	                   guild_ids=guild_ids,
	                   options=[
				   create_option(
                                	name = "search",
                                	description = "Search for wideo by url or keywords, support playlists",
                                	option_type = 3,
                                	required = True
                               	   ),
				   create_option(
                                	name = "random_order",
                                	description = "Toggle random order of videos to play, will apply only to playlists",
                                	option_type = 3,
                                	required = False,
					choices = [
						create_choice(name = 'Yes', value = 'True'), 
						create_choice(name = 'No', value = 'False')
				   	]
                               	   )])
	async def _play(self, ctx: SlashContext, search, random_order = None): 
		"""Request a song and add it to the queue.
		This command attempts to join a valid voice channel if the bot is not already in one.
		Uses YTDL to automatically search and retrieve a song.
		Parameters
		------------
		search: str [Required]
			The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
		"""
		#if random != None:
			#ytdlopts['playlistrandom'] = True
		#else:
			#ytdlopts['playlistrandom'] = False
		await ctx.defer()

		vc = ctx.voice_client

		if not vc:
			await ctx.invoke(self.connect_)

		player = self.get_player(ctx)
		# If download is False, source will be a dict which will be used later to regather the stream.
		# If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
		source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
		if source == "type_playlist":
			source = await YTDLSource.create_source_from_playlist(ctx, search, loop=self.bot.loop, download=False, player=player)
			return 0
		await player.queue.put(source)
		#await ctx.send( "NO play", hidden = True)
		
	@cog_ext.cog_slash(name="stop", 
	                   description="Stop playing music, clears queue and leave voice channel", 
	                   guild_ids=guild_ids,
	                   )
	async def stop_(self, ctx):
		"""Stop the currently playing song and destroy the player.
		!Warning!
			This will destroy the player assigned to your guild, also deleting any queued songs and settings.
		"""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently playing anything!', delete_after=20)
		
		await self.cleanup(ctx.guild)
	
	@cog_ext.cog_slash(name="console", 
	                   description="Open up a module-related console", 
	                   guild_ids=guild_ids,
			   options=[
				   create_option(
                                	name = "module",
                                	description = "Select module for console",
                                	option_type = 3,
                                	required = True,
					choices = [
						create_choice(name = 'Music', value = 'music'), 
						#create_choice(name = 'No', value = 'False')
				   	]
                               	   )]
	                   )
	async def console_(self, ctx, module):
		if module == 'music':
			#view = MusicButtons()
			buttons = [
				create_button(
                			style=ButtonStyle.blurple,
                			emoji="🎵",
					custom_id="music_current_song",
            			),
				create_button(
                			style=ButtonStyle.blurple,
                			emoji="🔀",
					custom_id="music_mix_songs",
            			),
				create_button(
                			style=ButtonStyle.blurple,
                			emoji="⏹️",
					custom_id="music_stop",
            			),
				create_button(
                			style=ButtonStyle.blurple,
                			emoji="⏯️",
					custom_id="music_pause_resume",
            			),
				create_button(
                			style=ButtonStyle.blurple,
                			emoji="⏭️",
					custom_id="music_skip_song",
            			),
          		]
			buttons_row_two = [
				create_button(
                			style=ButtonStyle.blurple,
                			#label="🎶"
					emoji="🎶",
					custom_id="music_queue",
            			),
				create_button(
					style=ButtonStyle.blurple,
					emoji="❔",
					custom_id="music_help",
				),
				create_button(
					style=ButtonStyle.blurple,
					emoji="🔁",
					custom_id="music_loop",
				),
				create_button(
					style=ButtonStyle.blurple,
					emoji="🔂",
					custom_id="music_song_loop",
				),
				create_button(
					style=ButtonStyle.blurple,
					emoji="🔇",
					custom_id="music_no_voice",
				),
			]
			embed = discord.Embed( 
				title="Music console",
				description="Use button for set action",
				color = 0x206694,
				timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
			)
			embed.add_field(name= 'Buttons', value="""🎶 : Display current queue \n
							          🎵 : Display information about current song \n
								  ⏹️ : Clear queue and leave voice channel \n
								  ⏯️ : Stops / Resumes playing songs \n
								  ⏭️ : Skips current song""", inline=True),
			embed.add_field(name= 'Buttons', value="``` TEST ```", inline=True),
			action_row_one = create_actionrow(*buttons)
			action_row_two = create_actionrow(*buttons_row_two)
			#if not vc or not vc.is_connected():
			#return await ctx.send('>>> There is no music playing right now', hidden = True)
			music_console_msg =  await ctx.send( embed = embed, components=[action_row_one, action_row_two])
			#music_console_msg =  await ctx.send( embed = embed,view=view)
			def check_button(i: discord.Interaction, button):
				#print(f'checking i.autor:{i.author} and ctx.autor: {ctx.author}, i.message: {i.message}, also music_console_msg: {music_console_msg}')
				#return i.author == ctx.author and i.message == music_console_msg
				return i.message.id == music_console_msg.id
			state = True
			while state:
				event, button = await self.client.wait_for("button_click", check=check_button) # , button
				#message_reference = await ctx.channel.fetch_message(music_console_msg)
				embed = discord.Embed(title='You pressed an Button',
					      description=f'You pressed a {button.emoji} button.',
					      color=discord.Color.random())
				#await ctx.send(embed=embed, delete_after = 60) #, reference = music_console_msg
				#await event.respond(embed = embed) #, delete_after = 5
				
				await event.channel.send(embed = embed, reference = music_console_msg)
				await event.respond(content='Test')
	
			
			#await client.wait_for("button_click", check = lambda i: i.component.emoi == '🎶')
			#interaction_queue = await client.wait_for("button_click", check=lambda i: i.component.emoi == '🎶')
			#await interaction_queue.response.send_message('QUEUE', delete_after = 5)
			#await test.respond(content="queue")

def setup(client: client):
	client.add_cog(Slash_music(client))
