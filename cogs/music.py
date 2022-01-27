import discord, json, io, os, typing, requests, random, asyncio, youtube_dl, psycopg2
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel, PCMVolumeTransformer
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot

from functions import get_prefix, get_time, get_database_data

#Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
	'format': 'bestaudio/best',
	'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
	'restrictfilenames': True,
	'noplaylist': True,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
	'force-ipv4': True
}

ffmpeg_options = {
	'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()


class YTDLSource(discord.PCMVolumeTransformer):
	def __init__(self, source, *, data, volume=0.5):
		super().__init__(source, volume)
		self.data = data
		self.title = data.get('title')
		self.url = data.get('url')

	@classmethod
	async def from_url(cls, url, *, loop=None, stream=False):
		loop = loop or asyncio.get_event_loop()
		data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

		if 'entries' in data:
			# take first item from a playlist
			data = data['entries'][0]
			
		filename = data['url'] if stream else ytdl.prepare_filename(data)
		return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
        
	@commands.Cog.listener()
	async def on_ready(self):
		print('Music module loaded')
#
#<----------> 'join' command - just 'n only join the channel <------------------------------------------------------------------------>
#
	@commands.command()
	async def join(self, ctx):
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return await ctx.send("Music is OFF on this guild!")
		if ctx.author.voice:
			if ctx.voice_client is not None:
				return await ctx.voice_client.move_to(ctx.author.voice.channel)
		else:
			await ctx.send("You are not connected to a voice channel.")

		await ctx.author.voice.channel.connect()
#
#<----------> 'downloadnplay' command - download before playing - more technick <------------------------------------------------------------------------>
#
	@commands.command()
	async def downloadnplay(self, ctx, *, url): 
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return await ctx.send("Music is OFF on this guild!")
		async with ctx.typing():
			player = await YTDLSource.from_url(url, loop=self.bot.loop)
			ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

		await ctx.send(f'Now playing: {player.title}')
		
	@downloadnplay.error
	async def downloadnplay_error(self, ctx: commands.Context, error):
		print(error)
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
		elif isinstance(error, commands.errors.ChannelNotFound):
			await ctx.channel.send("Channel not found!")
		elif isinstance (error, youtube_dl.utils.ExtractorError):
			await ctx.channel.send("Error with wideo download!")
		else: 
			await ctx.channel.send("There was an error with executing command!")
#
#<----------> 'play' command - play music on channel without pre-downloading <------------------------------------------------------------------------>
#
	@commands.command()
	async def play(self, ctx, *, url):
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return await ctx.send("Music is OFF on this guild!")
		volume = get_database_data('servers_data', 'music_volume', ctx.guild.id)
		player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
		try:
			async with ctx.typing():
				ctx.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)
				print( f'Now playing: {player.title} on: {ctx.guild} guild.')
			await ctx.send(f'Now playing: {player.title}')
			ctx.voice_client.source.volume = volume / 100
		except:
			print( f'Error while playing: {player.title} on: {ctx.guild} guild.')
			await ctx.send(f'There was some trouble to play: {player.title}. This can be program error, or this video may be inappropriate for some users.')
	@play.error
	async def play_error(self, ctx: commands.Context, error):
		print(error)
		if isinstance(error, commands.errors.MemberNotFound):
			await ctx.channel.send("Member not found!")
		elif isinstance(error, commands.errors.ChannelNotFound):
			await ctx.channel.send("Channel not found!")
		elif isinstance (error, youtube_dl.utils.ExtractorError):
			await ctx.channel.send("Error with wideo download!")
		else: 
			await ctx.channel.send("There was an error with executing command!")
#
#<----------> 'volume' command - change volume of music that is playing <------------------------------------------------------------------------>
#
	@commands.command()
	async def volume(self, ctx, volume: int):
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return await ctx.send("Music is OFF on this guild!")
		if ctx.voice_client is None:
			return await ctx.send("Bot is not connected to a voice channel.")
		if not volume <= 150:
			return await ctx.send("Sorry! There is a limit of 150.")
		database_record = get_database_data('servers_data', 'music_volume', ctx.guild.id)
		if volume == database_record:
			return await ctx.send(f"Volume already set to: {volume}%.")
		cur.execute("UPDATE servers_data SET music_volume = '{}' WHERE guild_id = '{}';".format(volume, ctx.guild.id))
		con.commit()
		if ctx.voice_client.source != None:
			ctx.voice_client.source.volume = volume / 100
			await ctx.send(f"Changed volume to {volume}%")
		else: 
			await ctx.send(f"Volume change to {volume}%, will take affect in next music play!")
#
#<----------> 'stop' command - leave from channel <------------------------------------------------------------------------>
#
	@commands.command()
	async def stop(self, ctx):
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return await ctx.send("Music is OFF on this guild!")
		await ctx.voice_client.disconnect()
		await ctx.send("Bot left voice channel.")

#
#<----------> before invoke - check if user is on channel <------------------------------------------------------------------------>
#
	@play.before_invoke
	@downloadnplay.before_invoke
	async def ensure_voice(self, ctx):
		database_record = get_database_data('servers_properties', 'music', ctx.guild.id)
		if database_record == 'NO':
			return 0
		if ctx.voice_client is None:
			if ctx.author.voice:
				await ctx.author.voice.channel.connect()
			else:
				await ctx.send("You are not connected to a voice channel.")
				raise commands.CommandError("Author not connected to a voice channel.")
		elif ctx.voice_client.is_playing():
			ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or(get_prefix))
    
def setup(client):
	client.add_cog(Music(client))
    
