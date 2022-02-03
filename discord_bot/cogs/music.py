"""
Please understand Music bots are complex, and that even this basic example can be daunting to a beginner.
For this reason it's highly advised you familiarize yourself with discord.py, python and asyncio, BEFORE
you attempt to write a music bot.
This example makes use of: Python 3.6
For a more basic voice example please read:
    https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
This is a very basic playlist example, which allows per guild playback of unique queues.
The commands implement very basic logic for basic usage. But allow for expansion. It would be advisable to implement
your own permissions and usage logic for commands.
e.g You might like to implement a vote before skipping the song or only allow admins to stop the player.
Music bots require lots of work, and tuning. Goodluck.
If you find any bugs feel free to ping me on discord. @Eviee#0666
"""
import discord
from discord.ext import commands

import asyncio
import itertools
import sys
import traceback
import psycopg2
import os
import functools
import math
import random
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
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
	'noplaylist': False, #True
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
	'before_options': '-nostdin',
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
			self.description = self.description[:75] + '...'
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
		if 'entries' in data:
			# take first item from a playlist
			id_list = []
			#data = []
			#iteration = 0
			for item in data['entries']:
				id_list.append(item['id'])
			print(f"Liczba id: {len(id_list)}")
			print(f"Lista id: {id_list}")
			data = data['entries'][0]
		
		embed = discord.Embed( 
			title="Added to queue",
			description="You can always check queue with *queue* command",
			color= message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.add_field(name= "Title:", value=data["title"], inline=True),
		embed.add_field(name= "Requested by:", value=ctx.author, inline=True),
		await ctx.send(embed = embed, delete_after=15)

		if download:
			source = ytdl.prepare_filename(data)
		else:
			return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}
		
		return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

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

#class Music:
"""Music related commands."""

	#__slots__ = ('bot', 'players')

	#def __init__(self, bot):
		#self.bot = bot
		#self.players = {}


class Music(commands.Cog):
	
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

	async def __error(self, ctx, error):
		"""A local error handler for all errors arising from commands in this cog."""
		if isinstance(error, commands.NoPrivateMessage):
			try:
				return await ctx.send('This command can not be used in Private Messages.')
			except discord.HTTPException:
				pass
		elif isinstance(error, InvalidVoiceChannel):
			await ctx.send('Error connecting to Voice Channel. '
							'Please make sure you are in a valid channel or provide me with one')

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

	@commands.command(name='connect', aliases=['join'])
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

	@commands.command(name='play', aliases=['sing'])
	async def play_(self, ctx, *, search: str):
		"""Request a song and add it to the queue.
		This command attempts to join a valid voice channel if the bot is not already in one.
		Uses YTDL to automatically search and retrieve a song.
		Parameters
		------------
		search: str [Required]
			The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
		"""
		await ctx.trigger_typing()

		vc = ctx.voice_client

		if not vc:
			await ctx.invoke(self.connect_)

		player = self.get_player(ctx)

		# If download is False, source will be a dict which will be used later to regather the stream.
		# If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
		source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
		await ctx.message.add_reaction('✅')
		await player.queue.put(source)
	"""	
	@commands.command(name='playlist', aliases=['sing_playlist'])
	async def playlist_(self, ctx, *, search: str):
		""""""Request a song and add it to the queue.
		This command attempts to join a valid voice channel if the bot is not already in one.
		Uses YTDL to automatically search and retrieve a song.
		Parameters
		------------
		search: str [Required]
			The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
		""""""
		await ctx.trigger_typing()

		vc = ctx.voice_client

		if not vc:
			await ctx.invoke(self.connect_)

		player = self.get_player(ctx)

		# If download is False, source will be a dict which will be used later to regather the stream.
		# If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
		source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

		await player.queue.put(source)"""

	@commands.command(name='pause')
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

	@commands.command(name='resume')
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

	@commands.command(name='skip')
	async def skip_(self, ctx):
		"""Skip the song."""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently playing anything!', delete_after=20)

		if vc.is_paused():
			pass
		elif not vc.is_playing():
			return

		vc.stop()
		await ctx.message.add_reaction('✅')
		await ctx.send(f'**`{ctx.author}`**: Skipped the song!')

	@commands.command(name='queue', aliases=['q', 'playlist'])
	async def queue_info(self, ctx):
		"""Retrieve a basic queue of upcoming songs."""
		vc = ctx.voice_client

		if not vc or not vc.is_connected():
			return await ctx.send('I am not currently connected to voice!', delete_after=20)

		player = self.get_player(ctx)
		if player.queue.empty():
			return await ctx.send('There are currently no more queued songs.')

		# Grab up to 5 entries from the queue...
		upcoming = list(itertools.islice(player.queue._queue, 0, 5))

		fmt = '\n'.join(f'**`{_["title"]}`**' for _ in upcoming)
		embed = discord.Embed(title=f'Upcoming - Next {len(upcoming)}', description=fmt)
		
		await ctx.message.add_reaction('✅')
		await ctx.send(embed=embed)

	@commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
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
		
		embed = discord.Embed( 
			title="Now playing",
			description="Information about now playing song",
			color= ctx.message.author.colour,
			timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
		)
		embed.set_thumbnail(url=vc.source.thumbnail)
		embed.add_field(name= chr(173), value=f"**Title**: {vc.source.title} \n**Duration**: {vc.source.duration}", inline=True),
		embed.add_field(name= chr(173), value=f"**Views**: {vc.source.views} \n**Likes**: {vc.source.likes}", inline=True),
		embed.add_field(name= '**Description**:', value=f"```{vc.source.description}```", inline=False),
		embed.add_field(name= '**Url**:', value=vc.source.url, inline=False),
		embed.add_field(name= chr(173), value=f"**Uploader**: {vc.source.uploader} \n**Upload date**: {vc.source.upload_date}", inline=True),
		embed.add_field(name= chr(173), value=f"**Tags**: {vc.source.tags} \n**Requested by**: {vc.source.requester}", inline=True),
		embed.set_footer(text="Provided by Wild West Post Office")
		await ctx.message.add_reaction('✅')
		player.np = await ctx.send(embed = embed)

	@commands.command(name='volume', aliases=['vol'])
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

	@commands.command(name='stop')
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
