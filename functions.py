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

#DATABASE_URL = os.environ['https://data.heroku.com/datastores/32b203de-0866-4825-80b1-2706bd239a23']

DATABASE_URL = os.environ.get('DATABASE_URL')
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

def get_prefix(client, message):
	cur.execute("SELECT guild_prefix from SERVERS_PROPERTIES WHERE guild_id={}".format(message.guild.id))
	row = cur.fetchone()
	prefix = row[0]
	
	print("Prefix downloaded succesfully as '{}' on '{}' guild.".format(prefix, message.guild))
	con.commit()
	return prefix

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

def get_time( specify = "DT" ):
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
	if( specify == "TT" ):
		return str(current_time)
	else if( specify == "DD" ):
		return str(current_date)
	else:
		return str(dateandtime)
		
	
