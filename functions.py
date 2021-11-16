import discord, json, io, os, typing, requests, random, asyncio
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

def get_prefix(client, message):
	with open('data.json', 'r') as f:
		prefixes = json.load(f)
		
	return prefixes[str(message.guild.id)]

def get_time(mode):
	now = datetime.now() + timedelta(hours=2)
	today = date.today()
	current_day = today.strftime("%d/%m/%Y")   #global current_day
	current_time = now.strftime("%H:%M:%S")    #global current_time
	if (mode == time):
		time = str(current_time)
		return str(time)
	elif (mode == date):
		date = str(current_day)
		return str(date)
	else:
		datetime = str(current_time) + " , " + str(current_day)
		return str(datetime)
		
	
