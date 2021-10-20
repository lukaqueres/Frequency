import discord, json, io, os, typing, requests, random, asyncio
from os import getenv
from dotenv import load_dotenv
from ffmpeg import *
from random import randrange, randint
from datetime import datetime, date, timedelta
from discord import member, DMChannel, FFmpegPCMAudio, TextChannel
from discord.ext import tasks, commands
from discord.utils import get
from youtube-dl import *
from discord.ext.commands import has_permissions, MissingPermissions, bot
#from youtube_dl import YoutubeDL

client = discord.Client()
client = commands.Bot(command_prefix = '$')
#client.remove.command("help")
#@commands.has_permissions(manage_messages=True)

now = datetime.now() + timedelta(hours=2)
today = date.today()
current_day = today.strftime("%d/%m/%Y")   #global current_day
current_time = now.strftime("%H:%M:%S")    #global current_time

@client.event #---------------------------------READY---------------------------------------------------------------------------------------------------------
async def on_ready():
  await client.change_presence(status=discord.Status.online, activity=discord.Game('Red Dead Redemption 2'))          #status online/offline  , activity=discord.Game('Red Dead Redemption 2')
  print('Bot successfully logged in')
  
async def status_change():
  await client.wait_until_ready()
  statuses = ["Red Dead Redemption 2", "Red Dead Redemption 1", "Red Dead Online", "Red Dead Revolver" ]
  while not client.is_closed():
    sleep_time = random.randint(1800,3600)
    status = random.choice(statuses)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
    print("Activity has been changed to: {}, and next change will be again after: {} seconds." .format(status, sleep_time))
    await asyncio.sleep(sleep_time)
client.loop.create_task(status_change())

@client.event #----------------------------------ANTY PHISHING-------------------------------------------------------------------------------------------------
async def on_message(message):
  await client.process_commands(message)
  
  global current_day
  global current_time
  black_listed = ['Free', 'free', 'Nitro', 'nitro', 'Discord', 'discord', 'giveaway', 'Giveaway', 'Skin', 'skin', 'CS:GO', 'Counter-Strike: Global Offensive', 'CS']
  black_listed_length = (len(black_listed))
  black_listed_words_number_detected = 0
  if (message.author == client.user):
    return
  if (('http' in message.content ) or ('https' in message.content)):
    for x in black_listed:
      if (x in message.content):
        black_listed_words_number_detected += 1
        if (black_listed_words_number_detected == 2):
          print("\nPosible scam by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(message.author, message.channel, message.guild, current_time, current_day))
          embed = discord.Embed(
            title="Możliwy scam",
            description=" ",
            color=0x0000ff,
          )
          embed.add_field(name="Użytkownik:", value=message.author, inline=True),
          embed.add_field(name="Serwer:", value=message.guild, inline=True),
          embed.add_field(name = chr(173), value = chr(173))
          embed.add_field(name="Data:", value=current_day, inline=True),
          embed.add_field(name="Godzina:", value=current_time, inline=True),
          embed.add_field(name = chr(173), value = chr(173))
          embed.add_field(name="Treść wiadomości:", value=message.content, inline=False),
          user = await client.fetch_user("429949201254842369")
          author = message.author
          role = discord.utils.get(author.guild.roles, name="🤐 Wyciszony")
          RDPchannel = client.get_channel(887604610972409906)
          RDPguild = client.get_guild(640181649463705650)
          if role in message.author.roles:
            await message.delete()
          else:
            await message.delete()
            await DMChannel.send(user, embed=embed)
            await client.add_roles(author, role)
            if message.guild == RDPguild:
              await RDPchannel.send(embed=embed)
  else:
    return
#---ANTY PHISHING-------------------------------------------------------------------------------------------------
  

#----------------------------------------------------------------------------------------COMMANDS-------------------------------------------------------------------------------------------------------------
load_dotenv()
players = {}

@client.command(pass_context=True)
async def play(ctx, url : str):
  global current_day
  global current_time
  print("\n User used play command: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
  
  voice_channel = ctx.author.voice.channel
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild) 
  guild = ctx.message.guild
  voice_client = guild.voice_client
  await voice_channel.connect()
  
  YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
  FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
  voice = get(client.voice_clients, guild=ctx.guild)

  if not voice.is_playing():
     with YoutubeDL(YDL_OPTIONS) as ydl:
      info = ydl.extract_info(url, download=False)
     URL = info['url']
     voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
     voice.is_playing()
  # check if the bot is already playing
  else:
    await ctx.send("Bot już gra")
    return
        
  #player = await voice_client.create_ytdl_player(url)
  #filename = await YTDLSource.from_url(url, loop=bot.loop)
  #voice_channel.play(source=filename))  #(executable="ffmpeg.exe", source=filename))
  #players[guild.id] = player
  #player.start()
    
@client.command(pass_context=True)
async def leave(ctx):
  voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
  if voice.is_connected():
      await voice.disconnect()
  else:
      await ctx.send('"Bot nie jest połączony z żadnym kanałem głosowym."')
  
  
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send('"Obecnie nic nie jest odtwarzane."')


@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send('"Obecnie nic nie jest zatrzymane."')

@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()
        
        
        
        
        
        
        
        
        
        
@client.command()
@has_permissions(manage_messages=True)
async def cytaty(ctx):
    print(" \nCytaty command has been used by member on:")
    channel  = ctx
    embed = discord.Embed(
        title="Czasy rewolwerowców i bandytów dobiegły końca. \nDziki zachód stał się legendą, a za istnieniem legend zawsze kryją się niezapomniane słowa. Aby je poznać musisz skorzystać ze zwoju na poczcie",
        description="   Po naciśnięciu reakcji, zostanie wysłany jeden z wielu cytatów z gier: \n   Red Dead Redemption, Red Dead Redemption 2 oraz Red Dead Online",
        color=0x0000ff,
        )
    amount = 1
    await ctx.channel.purge(limit = amount)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('📜')
    #await msg.add_reaction('🏷️')
    #await ctx.message.add_reaction('📜')                                                    Emoji do wysłanej wiadomości przez użytkownika
    #await ctx.send(' >>> Ta opcja niedługo będzie działać :scroll:')                         Zwykła wiadomość jako cytat

@client.command()
@has_permissions(manage_messages=True)
async def embed(ctx):
    now = datetime.now()
    today = date.today()
    current_day = today.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    print("\nEmbed has been triggered by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
    await ctx.channel.purge(limit = 1)
    embed = discord.Embed(
        #name="Lukaqueres"
        title="Nowości & Aktualności Red Dead Online",
        description=" Co tygodniowa aktualizacja RDO: 07.09.2021 - 13.09.2021",
        color=0x0000ff,
        )
    embed.add_field(name="Zniżki:", value="**-** 5 sztabek na licencję łowcy nagród \n**-** 30% zniżki na broszury ról \n**-** 40% zniżki na konie bretońskie\n**-** 40% zniżki na pasy na broń ról\n**-** 40% na amunicję i strzemiona\n**-** 50% na ostrogi", inline=True)
    embed.add_field(name="Aktualności", value="W tym tygodniu wydarzenia w grze swobodnej oraz tryb do broni przynosi 2 razy więcej dochodów jak i PD. W trakcie przestępstw krwawej forsy można zdobyć więcej *kapitali* niż zwykle. W tym tygodniu jest również dostępna odzież z poprzednich przepustek bandyty.", inline=True)
    embed.add_field(name="Witamy 3 odsłonę Klubu Rewolwerowca", value="\nCena wynosi 25 sztabek złota które zwracają się po osiągnęciu 25, maksymalnego poziomu. Możemy w niej zdobyć m. in. Nową kamizelkę, nóż, kurtkę, maskę czy końską grzywę.\nJest dostępna do 4 października 2021 ", inline=False)
    embed.add_field(name="Więcej", value="""**W tym tygodniu:**\n- Za dowolną modyfikację broni można zarobić 25 nabojów zapalających do strzelby jak i 200 nabojów express do rewolweru\n- Wszyscy gracze RDO którzy zalogują się w tym tygodniu dostaną 3 specjalne oleje z węża i 3 silne serum w ciągu 72 godzin.
                    \n\nPosiadacze 2 poprzednich odsłon Klubu Rewolwerowca którzy zakupią tą (3) odsłonę otrzymają 25 not kapitałowych i 10 darmowych szybkich podróży w ciągu 72 godzin od zakupu. \nPrzypominamy że posiadanie wszystkich 4 odsłon zapewni darmową hallowienową przepustkę.  """, inline=False)
    embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    embed.set_thumbnail(url="https://prod.cloud.rockstargames.com/global/Events/23152/171b3f1d-4598-4415-9151-957aa943388a.jpg")
    embed.set_footer(text="Miłej gry")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('🏷️')

@embed.error
async def embed_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        now = datetime.now()
        today = date.today()
        current_day = today.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")
        print("\n Embed has been triggered and didn't work by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
        print(" Reason: \"not enough permissions \"")
        await ctx.channel.purge(limit = 1)

@client.command()
@has_permissions(manage_messages=True)
async def purge(ctx, number : int ):
    now = datetime.now()
    today = date.today()
    current_day = today.strftime("%d/%m/%Y")
    current_time = now.strftime("%H:%M:%S")
    print("\n Purge with walue {} has been triggered by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(number, ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
    await ctx.channel.purge(limit = number)

@purge.error
async def purge_error(error, ctx):
    if isinstance(error, MissingPermissions):
        now = datetime.now()
        today = date.today()
        current_day = today.strftime("%d/%m/%Y")
        current_time = now.strftime("%H:%M:%S")
        print("\n Purge has been triggered and didn't work by: \" {} \" on: \" {} \" channel in: \" {} \" guild on \" {} {} \".".format(ctx.message.author, ctx.message.channel, ctx.message.guild, current_time, current_day))
        print(" Reason: \" not enough permissions \"")
        await ctx.channel.purge(limit = 1)













client.run('ODc1MjcxOTk1NjQ0ODQyMDA0.YRTGkQ.52s28D_CmdNtZm3g4_llDs4AV9E')
