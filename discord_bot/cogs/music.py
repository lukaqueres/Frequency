# Based on @Eviee#0666 project https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
import psycopg2
import os
import re
import functools
import math
import random
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, Embed, Intents
from datetime import datetime, date, timedelta

from functions import get_prefix, get_time, get_database_data

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)
bot = commands.Bot(command_prefix = get_prefix, intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

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

class Music(commands.Cog):
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
		print('Music module loaded')

	@commands.command(name='connect', usage='connect [channel]', brief='Connects bot to user channel or the specified one', description='Connects bot to user channel or to specified.\nUsage is: ``` connect [channel]```', aliases=['join'])
	async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
		"""Connect to voice.
		Parameters
		------------
		channel: discord.VoiceChannel [Optional]
			The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
			will be made.
		This command also handles moving the bot to different channels.
		"""
		if not channel:
			try:
				channel = ctx.author.voice.channel
			except AttributeError:
				raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

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

		await ctx.message.add_reaction('✅')
		await ctx.send(f'Connected to: **{channel}**', delete_after=20)

	@commands.command(name='play', usage='play < url/key-words/id >', brief='Play specified song or playlist.', description='If needed joins channel and stream provided song or playlist.\nCan play from warious of services.', aliases=['sing', 'p'])
	async def play_(self, ctx, *, search: str, random = None):
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
		async with ctx.typing():

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
		await ctx.message.add_reaction('✅')
		await player.queue.put(source)

	@commands.command(name='pause', usage='pause', brief='Pause currently song', description='Pause playing songs, and wait til resume command invoke. Only used when anything is playing, and isn\'t paused yet')
	async def pause_(self, ctx):
		"""Pause the currently playing song."""
		vc = ctx.voice_client

		if not vc or not vc.is_playing():
			return await ctx.send('I am not currently playing anything!', delete_after=20)
		elif vc.is_paused():
			return

		vc.pause()
		await ctx.message.add_reaction('✅')
		await ctx.send(f'**`{ctx.author}`**: Paused the song!')

	@commands.command(name='resume', usage='resume', brief='Resume paused song', description='Resume playing songs if paused.')
	async def resume_(self, ctx):
		"""Resume the currently paused song."""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently playing anything!', delete_after=20)
		elif not vc.is_paused():
			return

		vc.resume()
		await ctx.message.add_reaction('✅')
		await ctx.send(f'**`{ctx.author}`**: Resumed the song!')

	@commands.command(name='skip', usage='skip', brief='Skip now playing song', description='Skip currently playing song, if queue is empty it will skip and wait for more songs to play.')
	async def skip_(self, ctx):
		"""Skip the song."""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently playing anything!', delete_after=20)

		if vc.is_paused():
			pass
		elif not vc.is_playing():
			return
		title = vc.source.title
		vc.stop()
		await ctx.message.add_reaction('✅')
		await ctx.send(f'**`{ctx.author}`**: Skipped: {title}')

	@commands.command(name='queue', usage='queue', brief='Displays info about queue', description='Send an embed with total duration of queue, basic info about now playing song and next 1-9 songs.', aliases=['q', 'playlist'])
	async def queue_info(self, ctx):
		"""Retrieve a basic queue of upcoming songs."""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently connected to voice!', delete_after=20)

		player = self.get_player(ctx)
		if player.queue.empty():
			return await ctx.send('There are currently no more queued songs.')

		# Grab up to 9 entries from the queue...
		upcoming = list(itertools.islice(player.queue._queue, 0, 9)) # 100 = 9
		total_queue = list(player.queue._queue)
		total_queue_length = len(list(player.queue._queue))
		total_duration = 0
		for _ in total_queue:
			total_duration = total_duration + int(_['duration'])
		total_duration = YTDLSource.parse_duration(total_duration)
		#fmt = '\n\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
		embed = Embed(title="Queue",
			      description = 'List of next songs in queue',
			      colour = 0x0000ff,
			      timestamp=datetime.utcnow()
		)
		_ = upcoming[0]
		embed.set_thumbnail(url= _["thumbnail"])
		#embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)
		embed.add_field(name= "Now playing:", value=f"**Title**: {vc.source.title} \n**Duration**: {vc.source.duration}\n**Requester**: {vc.source.requester}", inline=False),
		embed.add_field(name= "Info:", value=f"**Total number of songs in queue**: {total_queue_length}\n**Total duration**: {total_duration}", inline=False),
		iteration = 0
		if total_queue_length < 10:
			for _ in upcoming:
				iteration = iteration + 1
				title = _["title"]
				duration = _["duration"]
				requester = _["requester"]
				embed.add_field(name= f"Position: {iteration}", value=f"**Title**: {title} \n**Duration**: {YTDLSource.parse_duration(duration)}\n**Requester**: {requester}", inline=True),
		
		if total_queue_length > 9:
			upcoming = list(itertools.islice(player.queue._queue, 0, 8))
			rest_number = total_queue_length - len(upcoming)
			rest_list = list(itertools.islice(player.queue._queue, len(upcoming), total_queue_length)) #, 8
			rest_duration = 0
			for item in rest_list:
				rest_duration = rest_duration + int(item["duration"])
			rest_duration = YTDLSource.parse_duration(rest_duration)
			for _ in upcoming:
				iteration = iteration + 1
				title = _["title"]
				duration = _["duration"]
				requester = _["requester"]
				embed.add_field(name= f"Position: {iteration}", value=f"**Title**: {title} \n**Duration**: {YTDLSource.parse_duration(duration)}\n**Requester**: {requester}", inline=True),
			embed.add_field(name= f"And: {rest_number} more", value=f"**Duration**: {rest_duration}", inline=True),
		
		embed.set_footer(text="Provided by Wild West Post Office")
		await ctx.message.add_reaction('✅')
		await ctx.send(embed=embed)

	@commands.command(name='now_playing', usage='now_playing', brief='Send embed with many useful information about currently playing song', description='Displays information about uploader, upload date, views, likes, tags, url, etc.', aliases=['np', 'current', 'currentsong', 'playing'])
	async def now_playing_(self, ctx):
		"""Display information about the currently playing song."""
		
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently connected to voice!', delete_after=20)

		player = self.get_player(ctx)
		if not player.current:
			return await ctx.send('I am not currently playing anything!')

		try:
			# Remove our previous now_playing message.
			await player.np.delete()
		except discord.HTTPException:
			pass
		
		views = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(vc.source.views))
		likes = re.sub(r'(?<!^)(?=(\d{3})+$)', r'.', str(vc.source.likes))
		
		tags = []
		full_tags = list(vc.source.tags)
		wanted_tags = list(vc.source.tags)
		missed_tags = 0
		if len(full_tags) > 10:
			not_full_tags = list(itertools.islice(vc.source.tags, 0, 10)) # 100 = 9
			wanted_tags = list(itertools.islice(vc.source.tags, 0, 10)) # 100 = 9
			missed_tags = len(full_tags) - len(not_full_tags)
		tags = " | ".join(wanted_tags)
		tags = (tags + f"\n**And {missed_tags} tags more**.")
		embed = discord.Embed( 
			title="Now playing",
			description="Information about now playing song",
			color= ctx.message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=vc.source.thumbnail)
		embed.add_field(name= chr(173), value=f"**Title**: {vc.source.title} \n**Duration**: {vc.source.duration}", inline=True),
		embed.add_field(name= chr(173), value=f"**Views**: {views} \n**Likes**: {likes}", inline=True),
		embed.add_field(name= '**Description**:', value=f"```{vc.source.description}```", inline=False),
		embed.add_field(name= '**Url**:', value=vc.source.url, inline=False),
		embed.add_field(name= chr(173), value=f"**Uploader**: {vc.source.uploader} \n**Upload date**: {vc.source.upload_date}", inline=True),
		embed.add_field(name= chr(173), value=f"**Tags**: {tags} \n**Requested by**: {vc.source.requester}", inline=True),
		embed.set_footer(text="Provided by Wild West Post Office")
		await ctx.message.add_reaction('✅')
		player.np = await ctx.send(embed = embed)

	@commands.command(name='volume', usage='volume < ammount >', brief='Changes volume of songs', description='Change volume in %. Must estimate beetwen 1 and 100.', aliases=['vol'])
	async def change_volume(self, ctx, *, vol: float):
		"""Change the player volume.
		Parameters
		------------
		volume: float or int [Required]
			The volume to set the player to in percentage. This must be between 1 and 100.
		"""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently connected to voice!', delete_after=20)

		if not 0 < vol < 101:
			return await ctx.send('Please enter a value between 1 and 100.')

		player = self.get_player(ctx)

		if vc.source:
			vc.source.volume = vol / 100

		player.volume = vol / 100
		await ctx.message.add_reaction('✅')
		await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')

	@commands.command(name='stop', usage='stop', brief='Stops playing, and quit voice channel', description='When invoked clears queue, now playing song and quits channel.')
	async def stop_(self, ctx):
		"""Stop the currently playing song and destroy the player.
		!Warning!
			This will destroy the player assigned to your guild, also deleting any queued songs and settings.
		"""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently playing anything!', delete_after=20)
		
		await ctx.message.add_reaction('✅')
		await self.cleanup(ctx.guild)

	"""@connect_.before_invoke
	@play_.before_invoke
	async def ensure_voice_state(self, ctx: commands.Context):
		if not ctx.author.voice or not ctx.author.voice.channel: 
			raise commands.CommandError('You are not connected to any voice channel.')
			return await ctx.send('You are not connected to voice channel.')

		if ctx.voice_client:
			if ctx.voice_client.channel != ctx.author.voice.channel:
				raise commands.CommandError('Bot is already in a voice channel.')
				return await ctx.send('Bot is already in voice channel.')"""

def setup(client):
	client.add_cog(Music(client))
