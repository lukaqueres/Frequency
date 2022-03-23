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

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

def get_prefix(client, message):
	cur.execute("SELECT guild_prefix from SERVERS_PROPERTIES WHERE guild_id={}".format(message.guild.id))
	row = cur.fetchone()
	prefix = row[0]
	con.commit()
	#print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	return prefix

def get_database_data(database, column, condition):
	cur.execute("SELECT {} from {} WHERE guild_id={}".format(column, database, condition))
	row = cur.fetchone()
	value = row[0]
	con.commit()
	#print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	return value

def write_database_data(database, column, condition, value):
	cur.execute("UPDATE {} SET {} = '{}' WHERE guild_id = '{}';".format(database, column, value, condition))
	con.commit()
	return 1

def get_language(condition):
	cur.execute("SELECT guild_language from SERVERS_PROPERTIES WHERE guild_id={}".format(condition))
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
	for i in enumerate(ids):
		id_list.append(i[0])
	#return id_list
	return [688803708577775619, 812295569808162856, 499285265551065098, 930559672715464764]
	
