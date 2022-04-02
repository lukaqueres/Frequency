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

intents = discord.Intents.default()
intents.members = True

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

def get_prefix(client, message):
	cur.execute(
		"SELECT guild_prefix FROM SERVERS_PROPERTIES WHERE guild_id=%s",
		(message.guild.id, )
	)
	row = cur.fetchone()
	prefix = row[0]
	con.commit()
	#print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	return prefix

client = commands.Bot(command_prefix = get_prefix, intents=intents)

def get_database_data(database, column, condition):
	cur.execute("SELECT {} from {} WHERE guild_id={}".format(column, database, condition))
	#cur.execute(
	#	"SELECT %s FROM %s WHERE guild_id=%s",
	#	(column, database, condition)
	#)
	row = cur.fetchone()
	value = row[0]
	con.commit()
	#print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	return value

def write_database_data(database, column, condition, value):
	cur.execute(
		"UPDATE %s SET %s = %s WHERE guild_id = %s;",
		(database, column, value, condition)
	)
	con.commit()
	return 1

def get_language(condition):
	cur.execute(
		"SELECT guild_language FROM SERVERS_PROPERTIES WHERE guild_id=%s",
		(condition, )
	)
	row = cur.fetchone()
	language = row[0]
	con.commit()
	#print("Language downloaded succesfully as '{}' on '{}' guild.".format(prefix, condition))
	return language
"""
<---------->CODE USE JSON WHEN NEEDED <---------------------------------------------------------------------------------------->

def get_prefix(client, message):
	default = '$'
	with open('data.json', 'r') as f:
		prefixes = json.load(f)
		#prefix = prefixes[str(message.guild.id)]
	#if prefixes[str(message.guild.id)] is None:
	#	print("Forced default prefix on {}." .format(ctx.guild))
	#	return default
	#else:
	#	return prefixes[str(message.guild.id)]
	return prefixes[str(message.guild.id)]
"""

def get_time( specify = "DT", return_type = "str" ):
	wintertime = True
	summertime = False
	if (wintertime == True):
		now = datetime.now() + timedelta(hours=1)
		
		
	else:
		now = datetime.now() + timedelta(hours=2)
	
	today = date.today()
	current_day = today.strftime("%d/%m/%Y")   #global current_day
	current_time = now.strftime("%H:%M:%S")    #global current_time
	dateandtime = str(current_time) + " , " + str(current_day)
	if return_type == "str":
		if( specify == "TT" ):
			return str(current_time)
		elif( specify == "DD" ):
			return str(current_day)
		else:
			return str(dateandtime)
	elif return_type == "date":
		if( specify == "TT" ):
			return current_time
		elif( specify == "DD" ):
			return current_day
		else:
			return 0
		
def get_guilds_ids():
	cur.execute("SELECT guild_id from SERVERS_PROPERTIES") # WHERE 1
	ids = cur.fetchall()
	con.commit()
	id_list = []
	for row in ids:
    		id_list.append(row[0])
	#return id_list
	return [688803708577775619, 812295569808162856, 499285265551065098, 930559672715464764]
	
def check_database(guilds):
	print('Database check start:')
	report = ""
	tables = [ "SERVERS_PROPERTIES", "SERVERS_DATA", "SERVERS_MSG_PROCESS"]
	listofnames = []
	for guild in guilds:
		listofnames.append(guild.name)
	#print(f'Checking guilds: {listofnames} ')
	guilds_id = []
	default_prefix = '$'
	default_language = 'ENG'
	for guild in guilds:
		guild_report = ""
		guild_report += f"\nChecking guild: {guild.name}"
		correct_tables = 0
		for table in tables:
			SQL = """SELECT COUNT(*) FROM %s WHERE guild_id = %s"""
			data = (table, guild.id)
			cur.execute(SQL, data)
			row = cur.fetchone()
			#print(f"row: {row}")
			value = row[0]
			con.commit()
			if value == 1:
				correct_tables += 1
			else:
				guild_report += f"\n	Table {table} incorrect"
		guild_report += f"\nCorrect {correct_tables} out of {len(tables)}"
		#bot_user = client.get_user(client.user.id)
		date_of_join = str("{") + str(datetime.now()) + str("}")
		members_count = len([m for m in guild.members if not m.bot]) # doesn't include bots 
		guilds_id.append(guild.id)
		print('Database Check: Guild {} check.'.format( guild ))
		#>>> SQL = "INSERT INTO authors (name) VALUES (%s);" # Note: no quotes
		#>>> data = ("O'Reilly", )
		#>>> cur.execute(SQL, data)
		SQL = """
			INSERT INTO SERVERS_PROPERTIES
    				( GUILD_ID, GUILD_NAME, DATE_OF_JOIN, GUILD_PREFIX, NUMBER_OF_USERS, message_check_feature, ECONOMY, MUSIC, UPDATES, NUMBER_OF_MEMBERS, GUILD_LANGUAGE)
			SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
				WHERE
    					NOT EXISTS (
        					SELECT guild_id FROM SERVERS_PROPERTIES WHERE guild_id = %s
					);
			INSERT INTO SERVERS_DATA
    				( guild_id, guild_name, music_volume)
			SELECT %s, %s, %s
				WHERE
    					NOT EXISTS (
        					SELECT guild_id FROM SERVERS_DATA WHERE guild_id = %s
					);
			INSERT INTO SERVERS_MSG_PROCESS
    				( guild_id, guild_name )
			SELECT %s, %s
				WHERE
    					NOT EXISTS (
        					SELECT guild_id FROM SERVERS_MSG_PROCESS WHERE guild_id = %s
					);
		   """
		data = (guild.id, guild.name, date_of_join, default_prefix, guild.member_count, "NO", "NO", "YES", "NO", members_count, default_language, guild.id,
			guild.id, guild.name, 50, guild.id,
			guild.id, guild.name, guild.id
		       )
		cur.execute(SQL, data)
		con.commit()
		guild_report += f"\nCorrected data for guild {guild.name}"
		report += guild_report
	print(report)
	print("Succesful database actualization")
