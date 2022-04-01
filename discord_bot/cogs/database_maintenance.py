import discord, json, io, os, typing, requests, random, asyncio, psycopg2
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
from discord.ext import tasks, commands
from discord.utils import get
from youtube_dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot

from discord_slash import SlashCommand

from functions import get_prefix, get_time, get_database_data

load_dotenv()

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)
#client = discord.ext.commands.Bot

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

global check_database_on_startup
check_database_on_startup = False

#
#<----------> Check database <------------------------------------------------------------------------>
#

def check_database():
	print('Database check start:')
	listofnames = []
	for guild in client.guilds:
		listofids.append(guild.name)
	print(f'Checking guilds: {listofnames} ')
	guilds_id = []
	default_prefix = '$'
	default_language = 'ENG'
	for guild in client.guilds:
		date_of_join = str("{") + client.user.joined_at.strftime("%d/%m/%Y %H:%M:%S") + str("}")
		members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots 
		guilds_id.append(guild.id)
		print('Database Check: Guild {} check.'.format( guild ))
		cur.execute(
			"""
			IF NOT EXISTS (
				SELECT 1 FROM servers_properties WHERE guild_id = %s
			)
			INSERT INTO SERVERS_PROPERTIES (
				GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX,
				NUMBER_OF_USERS, message_check_feature, ECONOMY, MUSIC,
				UPDATES, NUMBER_OF_MEMBERS, GUILD_LANGUAGE
			)
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

			IF EXISTS (
				SELECT 1 FROM servers_properties WHERE guild_id = %s
			)
			INSERT INTO SERVERS_PROPERTIES (
				NUMBER_OF_USERS, NUMBER_OF_MEMBERS, GUILD_LANGUAGE
			)
			WHERE guild_id = %s
			VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);

			IF EXISTS (
			   SELECT 1 FROM servers_msg_process WHERE guild_id = %s
			)
			INSERT INTO servers_msg_process (
			   guild_id, guild_name
			)
			VALUES (%s, %s);
			""", (
				guild.id, guild.id, guild.name, date_of_join, default_prefix,
				guild.member_count, "NO", "NO", "YES", "NO", members_count,
				default_language, guild.id, guild.id, members_count,
				guild.member_count, default_language, guild.id, guild.id,
				guild.name
			)
		)
		con.commit()
		print(f"Succesful database actualization for guild {guild.name}")

#
#<=========> Cog start <===============================================================================>
#

class Database_maintenance(commands.Cog):
	def __init__(self, client):
		self.client = client
    
	@commands.Cog.listener()
	async def on_ready(self):
		print('Database maintenance module loaded')
		if check_database_on_startup:
			listofids = []
			for guild in client.guilds:
				listofids.append(guild.id)
			print(f"ID serwerów z botem: {listofids}")
			print(f"client.guilds: {client.guilds}")
			check_database()
    
#
#<----------> On Bot join to guild <-------------------------------------------------------------------->
#
	@commands.Cog.listener()
	async def on_guild_join(self, guild):
		print("Bot joined in guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
		default_prefix = '$'
		default_language = 'ENG'
		members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots
		date_of_join = str("{") + get_time("DD") + str("}")
		cur.execute(
			"""
			SET datestyle = dmy;

			INSERT INTO servers_properties (
				GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX,
				NUMBER_OF_USERS, message_check_feature, ECONOMY, MUSIC,
				UPDATES, NUMBER_OF_MEMBERS, GUILD_LANGUAGE
			)
			VALUES (
				%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
			);

			INSERT INTO servers_data ( guild_id, guild_name )
			VALUES (%s, %s);

			INSERT INTO servers_msg_process ( guild_id, guild_name )
			VALUES (%s, %s);
			""", (
				guild.id, guild.name, date_of_join, default_prefix,
				guild.member_count, "NO", "NO", "YES", "NO", members_count,
				default_language, guild.id, guild.name, guild.id, guild.name
			)
		)
		con.commit()
		print("Succesful data base registration.")
		slash = SlashCommand(client, sync_commands=True)
		print("Synced slash commands.")
    #
#<----------> On Bot remove from guild <----------------------------------------------------------------->
#
	@commands.Cog.listener()
	async def on_guild_remove(self, guild):
		print("Bot removed from guild: \" {} \" guild on \" {} \".".format(guild, get_time()))
		sql = """DELETE FROM servers_properties WHERE GUILD_ID = %s;
             DELETE FROM servers_data WHERE GUILD_ID = %s;
	     DELETE FROM servers_msg_process WHERE GUILD_ID = %s;"""
		guild = (guild.id, guild.id, guild.id)
		cur.execute(sql, guild)
		con.commit()
		print("Succesful data base registration.")
    
#
#<----------> On User join to guild <-------------------------------------------------------------------->
#
	@commands.Cog.listener()
	async def on_member_join(self, member):
		guild = member.guild.id
		members_count = len([m for m in member.guild.members if not m.bot]) # doesn't include bots
		#print("\n Member joined: \" {} \" guild on \" {} \".".format(member.guild.name, get_time()))
		cur.execute(
			"""
			SET datestyle = dmy;

			UPDATE SERVERS_PROPERTIES
			SET (NUMBER_OF_USERS, NUMBER_OF_MEMBERS) = (%s, %s)
			WHERE GUILD_ID = %s
			""", (members_count, member.guild.member_count, guild)
		)
		con.commit()

#
#<----------> On User leave from guild <----------------------------------------------------------------->
#
	@commands.Cog.listener()
	async def on_member_remove(self, member):
		guild = member.guild.id
		members_count = len([m for m in member.guild.members if not m.bot]) # doesn't include bots
		#print("\n Member left: \" {} \" guild on \" {} \".".format(member.guild.name, get_time()))
		cur.execute(
			"""
			SET datestyle = dmy;

			UPDATE SERVERS_PROPERTIES
			SET (NUMBER_OF_USERS, NUMBER_OF_MEMBERS) = (%s, %s)
			WHERE GUILD_ID = %s
			""", (members_count, member.guild.member_count, guild)
		)
		con.commit()
    

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		guild = channel.guild
		guild_id = guild.id
		channel_id = channel.id
		database_record_channel_one = get_database_data('servers_data', 'message_check_channel_id', guild_id)
		database_record_channel_two = get_database_data('servers_data', 'updates_channel_id', guild_id)
		database_record_channel_three = get_database_data('servers_data', 'logs_msg_channel_id', guild_id)
		null = 'NULL'
		if (channel_id == database_record_channel_one):
			cur.execute(
				"""
				UPDATE servers_data
				SET message_check_channel_id = %s
				WHERE GUILD_ID = %s
				""", ('NULL', guild_id)
			)
			con.commit()
			cur.execute(
				"""
				UPDATE servers_properties
				SET message_check_feature = %s
				WHERE GUILD_ID = %s
				""", ('NO', guild_id)
			)
			con.commit()
		elif (channel_id == database_record_channel_two):
			cur.execute(
				"""
				UPDATE servers_data
				SET updates_channel_id = %s
				WHERE GUILD_ID = %s
				""", ('NULL', guild_id)
			)
			con.commit()
			cur.execute(
				"""
				UPDATE servers_properties
				SET updates = %s
				WHERE GUILD_ID = %s
				""", ('NO', guild_id)
			)
			con.commit()
		elif (channel_id == database_record_channel_three):
			cur.execute(
				"""
				UPDATE servers_data
				SET logs_msg_channel_id = %s
				WHERE GUILD_ID = %s
				""", ('NULL', guild_id)
			)
			con.commit()
		else:
			return 0
    
def setup(client):
	client.add_cog(Database_maintenance(client))
