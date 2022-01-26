import discord, json, io, os, typing, requests, random, asyncio, psycopg2, nltk
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

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

from functions import get_prefix, get_time

load_dotenv()

intents = discord.Intents().all()
intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = get_prefix, intents=intents)

DATABASE_URL = os.environ.get('DATABASE_URL') 
con = psycopg2.connect(DATABASE_URL)
cur = con.cursor()

#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')

stop_words = set(stopwords.words('english'))

class Neurolinguistic_AI(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Neurolinguistic AI module loaded')
	
	@commands.Cog.listener()
	async def on_message(self, message):
		#if '875271995644842004' in message.content:
		if message.content.startswith('<@!875271995644842004>'):
			text = message.content
			tokenized = sent_tokenize(text)
			# sent_tokenize is one of instances of
			# PunktSentenceTokenizer from the nltk.tokenize.punkt module
			for i in tokenized:
				# Word tokenizers is used to find the words
				# and punctuation in a string
				wordsList = nltk.word_tokenize(i)
				# removing stop words from wordList
				wordsList = [w for w in wordsList if not w in stop_words]
				# Using a Tagger. Which is part-of-speech
				# tagger or POS-tagger.
				tagged = nltk.pos_tag(wordsList)
				print(tagged)
			#do nothin'g
		
def setup(client):
	client.add_cog(Neurolinguistic_AI(client))
