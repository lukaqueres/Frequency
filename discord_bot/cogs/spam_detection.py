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

from functions import get_prefix, get_time, get_database_data

client = commands.Bot(command_prefix = get_prefix)

load_dotenv()

class Spam_detection(commands.Cog):
  def __init__(self, client):
  	self.client = client
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Spam detection module loaded')
    
  @commands.Cog.listener()
  async def on_message(self, message):
    #await client.process_commands(message)
    guild_id = message.guild.id
    database_record = get_database_data('servers_properties', 'anty_spam_feature', guild_id)
    black_listed = ['Gift', 'gift', 'Steam', 'steam', 'Free', 'free', 'Nitro', 'nitro', 'Discord', 'discord', 'giveaway', 'Giveaway', 'Skin', 'skin', 'CS:GO', 'Counter-Strike: Global Offensive', 'CS']
    black_listed_length = (len(black_listed))
    black_listed_words_number_detected = 0
    if database_record == 'NO':
      return 0
    alert_channel_id = get_database_data('servers_data', 'anty_spam_channel_id', guild_id)
    alert_channel = self.client.get_channel( id = alert_channel_id )
    if (message.author == client.user):
      return
    if (('http' in message.content ) or ('https' in message.content)):
      for x in black_listed:
        if (x in message.content):
          black_listed_words_number_detected += 1
          if (black_listed_words_number_detected == 2):
            message_state = 'Define'
            try:
              await message.delete()
              message_state = 'deleted'
              #print("Message deleted")
            except commands.errors.MessageNotFound:
              message_state = 'not found'
            except:
              #print("Message not deleted")
              message_state = 'not deleted'
            print("\nPosible scam by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} \". Message {}.".format(message.author, message.channel, message.guild, get_time(), message_state))
            message_state = message_state.capitalize()
            message_content = ('||' + message.content + '||')
            embed = discord.Embed( 
              title="Message flagged",
              description=" ",
              color=0x0000ff,
              timestamp=datetime.utcnow() + timedelta( hours = 0 ) #timestamp=datetime.datetime.utcnow() + timedelta( hours = 1 )
            )
            embed.add_field(name= chr(173), value=f"**User**: {message.author} \n**User ID**: {message.author.id}", inline=True),
            embed.add_field(name= chr(173), value=f"**Channel**: {message.channel} \n**Channel ID**: {message.channel.id}", inline=True),
            embed.add_field(name="Message content:", value=message_content, inline=False),
            embed.add_field(name=chr(173), value=f"**Message status**: {message_state}", inline=False),
            await alert_channel.send(embed=embed)
    else: 
      return
    
def setup(client):
  client.add_cog(Spam_detection(client))
