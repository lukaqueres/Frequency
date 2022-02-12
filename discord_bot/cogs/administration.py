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

from functions import get_prefix, get_time

load_dotenv()

class Administration(commands.Cog):
  """Commands related for administrators and moderators to help with guild aministration"""
  
  def __init__(self, client):
  	self.client = client 
    
  @commands.Cog.listener()
  async def on_ready(self):
    print('Administration module loaded')
  
  @commands.command(name='ban', usage='ban <member> [reason]', brief='Ban specified user.', description='Bans selected member. It is possible to ban without reason, but you can still provide it.')
  @commands.has_permissions(ban_members = True)
  async def ban(ctx, user : discord.Member, *, reason = None):
    await member.ban(reason = reason)
    print("Member {member} banned on {ctx.guild} guild on {get_time()} .")

  @commands.command(name='unban', usage='ban <member>', brief='Clear ban specified user.', description='Un-bans selected member. Remember that you can\'t un-ban nto banned user.')
  @commands.has_permissions(ban_members = True)
  async def unban(ctx, user : discord.Member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
      user = ban_entry.user

      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        print("Member {member} unbanned on {ctx.guild} guild on {get_time()} .")
        await ctx.send(f'Unbanned {user.mention}')
        return
    
def setup(client):
  client.add_cog(Administration(client))
