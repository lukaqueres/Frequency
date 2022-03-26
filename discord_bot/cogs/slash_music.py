import discord, json, io, os, typing, requests, random, asyncio
from discord import member, DMChannel, TextChannel, Intents
from discord.ext import tasks, commands
from discord.utils import get
from discord import Embed
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, SlashCommand
from discord_slash.utils.manage_commands import create_choice, create_option
from discord.ext.commands import has_permissions, MissingPermissions

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
client = commands.Bot(command_prefix = get_prefix, Intents=intents)

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
	def __init__(self, client: Bot):
		self.client = client
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Slash music module loaded')
		
	#music = client.create_group("music", "Music related commands.")

	@cog_ext.cog_slash(name="connect", 
	                   description="Connect to voice channel", 
	                   guild_ids=guild_ids,
	                   options=[
				   create_option(
                                	name = "channel",
                                	description = "Choose voice channel to connect, if not specified, bot will join current user channel",
                                	option_type = 7,
                                	required = False,
                               	   )])
	@commands.has_permissions(manage_messages=True)
	async def _connect(self, ctx: SlashContext, channel = None): 
		await ctx.send( "Channel", hidden = True)
	
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
                                	name = "random",
                                	description = "Toggle random order of videos to play, will apply only to playlists",
                                	option_type = 5,
                                	required = False,
					choices = [
						create_choice(name = 'Yes', value = True), 
						create_choice(name = 'No', value = False)
				   	]
                               	   )])
	@commands.has_permissions(manage_messages=True)
	async def _play(self, ctx: SlashContext, search = None, random = None): 
		ctx.send( "NO play", hidden = True)
def setup(client: client):
	client.add_cog(Slash_music(client))
