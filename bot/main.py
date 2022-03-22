### Libraries ###
import discord
from discord.ext import commands
from pretty_help import DefaultMenu, PrettyHelp

from asyncio import sleep
import os
import random
import re

import smtplib, ssl 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

from discord.utils import get
from discord.utils import find
from discord.ext.commands import Bot

from discord.ext import tasks

import aiohttp
import json
import jsonpickle
from json import JSONEncoder

from configparser import *
### End Libraries ###


# Global variables
SKIP_BOTS = False

intents = discord.Intents.all()

nav = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")

ending_note = "{ctx.bot.user.name} is not affiliated with QUT"

bot = commands.Bot(command_prefix="qut!", description="A bot to help with QUT servers", intents=intents)
client = discord.Client
Client = Bot('qut!')

bot.help_command = PrettyHelp(menu=nav, color=discord.Colour.blue(), ending_note=ending_note)

token = os.getenv("DISCORD_TOKEN")

codes = []

config = ConfigParser()

version = "QUTBot v1.3.1"
changelog = "- Adjusted verification regex\n\nCheckout the code on Github: **https://github.com/Mistyttm/DiscordQUTVerificationBot**"

#moderation commands
class Moderation(commands.Cog):
  """All Moderation Commands"""
  
  def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization':f'Bot {token}',
            'User-Agent':'DiscordBot (https://discord.com/api/oauth2/authorize?client_id=953211624066539541&permissions=8&scope=bot) Python/3.10 aiohttp/3.8.1',
            'Content-Type':'application/json'
        }

  @commands.command(
    name="test",
    brief="test",
    help="test"
  )
  async def _test(self, ctx):
    num = random.randint(1,100)
    await ctx.send(f"{ctx.message.author.mention} your number is {num}")
  
  #@commands.command(
  #  name="events",
  #  brief="Make an event",
  #  help="Command to create an event"
  #)
  #async def create_guild_event(
  #      self,
  #      guild_id: str,
  #      event_name: str,
  #      event_description: str,
  #      event_start_time: str,
  #      event_end_time: str,
  #      event_metadata: str,
  #      event_privacy_level=2,
  #      channel_id=None
  #  ) -> None:
  #      '''Creates a guild event using the supplied arguments
  #      The expected event_metadata format is event_metadata={'location': 'YOUR_LOCATION_NAME'}
  #      The required time format is %Y-%m-%dT%H:%M:%S'''
  #      event_create_url = f'{self.base_api_url}/guilds/{guild_id}/scheduled-events'
  #      event_data = json.dumps({
  #          'name': event_name,
  #          'privacy_level': event_privacy_level,
  #          'scheduled_start_time': event_start_time,
  #          'scheduled_end_time': event_end_time,
  #          'description': event_description,
  #          'channel_id': channel_id,
  #          'entity_metadata': {'location': f'{event_metadata}'},
  #          'entity_type': 3
  #      })
  #      async with aiohttp.ClientSession(headers=self.auth_headers) as session:
  #          try:
  #              async with session.post(event_create_url, data=event_data) as response:
  #                  response.raise_for_status()
  #                  assert response.status == 200
  #          except Exception as e:
  #              print(f'EXCEPTION: {e}')
  #          finally:
  #              await session.close()

  #@commands.command(
  #  name='clear',
  #  brief='Clears messages',
  #  help='this command will clear msgs'
  #)
  #async def clear(ctx, number):
  #  mgs = [] #Empty list to put all the messages in the log
  #  number = int(number) #Converting the amount of messages to delete to an integer
  #  async for x in Client.logs_from(ctx.message.channel, limit = number):
  #      mgs.append(x)
  #  await Client.delete_messages(mgs)

# commands for information
class Info(commands.Cog):
  """Information commands"""
  @commands.command(
    name="info",
    brief="Info about the bot",
    help="Command to provide information about the bot"
  )
  async def _info(self, ctx):
    global version
    embed=discord.Embed(title="f{version}", url="https://github.com/Mistyttm/DiscordQUTVerificationBot", description=f"This bot was designed and programmed by *Emmey Leo* for the QUT IN01 Discord. It provides a system to verify that new members are qut students. This project is completely open source and any and all people are allowed to contribute to the github:\n\n**https://github.com/Mistyttm/DiscordQUTVerificationBot**", color=discord.Color.dark_blue())
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
    await ctx.send(embed=embed)
    
  @commands.command(
    name="changelog",
    brief="Shows the changelog",
    help="Command to show all the changes in the current version of QUTBot"
  )
  async def _changelog(self, ctx):
    global version
    global changelog
    embed=discord.Embed(title=f"{version} Changelog", url="https://github.com/Mistyttm/DiscordQUTVerificationBot", description=f"{changelog}", color=discord.Color.dark_blue())
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
    embed.set_author(name="Emmey", icon_url="https://cdn.discordapp.com/attachments/835791348291469342/954362018884886528/IMG_20220303_125955_403.jpg")
    await ctx.send(embed=embed)
  
  @commands.command(
    name="bug",
    brief="Gives new issue submission link",
    help="Command to provide the issues link for the QUTBot GitHub"
  )
  async def _bug(self, ctx):
    embed=discord.Embed(title=f"{version} Issue report", url="https://github.com/Mistyttm/DiscordQUTVerificationBot", description=f"Please go to this site and fill out a bug report:\n\nhttps://github.com/Mistyttm/DiscordQUTVerificationBot/issues/new/choose", color=discord.Color.red())
    await ctx.send(embed=embed)
  
  @commands.command(
    name="hiq",
    brief="Sends link to HiQ",
    help="Command to send the link directly to the HiQ homepage"
  )
  async def _hiq(self, ctx):
    embed=discord.Embed(title=f"{version} HiQ", url="https://github.com/Mistyttm/DiscordQUTVerificationBot", description=f"HiQ:\n\nhttps://qutvirtual4.qut.edu.au/group/student/home", color=discord.Color.dark_blue())
    embed.set_thumbnail(url="https://qutvirtual4.qut.edu.au/image/image_gallery?uuid=acca9ca6-6d8c-4643-9351-d2f2c2b450eb&groupId=13901&filename=HiQlogo.jpg&t=1581892242556")
    await ctx.send(embed=embed)
  
# Commands for verification
class Verify(commands.Cog):
  """Verification commands"""
  @commands.command(
    name="verify",
    brief="Instructions on how to verify",
    help="Command to provide information about how to verify your account"
  )
  async def _info(self, ctx):
    embed=discord.Embed(title="Verification Instructions", url="https://github.com/Mistyttm/DiscordQUTVerificationBot", description=f"1. Go to #verification\n2. Send your student number e.g. n12345678\n3. Check your QUT email for the verification code\n4. Send the verification code in #verification", color=discord.Color.dark_blue())
    await ctx.send(embed=embed)
  

#class Verification(commands.Cog):
#  """All Verification Commands"""
#  @commands.command(
#    name="clearcodes",
#    brief="Clears verification codes",
#    help="This command removes all stored verification codes, users who have not used their code will need another one"
#  )
#  async def _removeCodes(self, ctx):
#    global codes
#    codes.clear()
#    print(codes)
#    await ctx.send("All verification codes have been deleted")

#  @commands.command(
#    name="addcode",
#    brief="Adds a custom code",
#    help="This command adds a custom 4 number code for moderators to give out"
#  )
#  async def _addCodes(self, ctx, arg,):
#    global codes
#    role = discord.utils.find(lambda r: r.name == 'Moderator', ctx.message.guild.roles)
#    if len(arg) == 4 and role in self.roles:
#      codes.append(arg)
#      print(codes)
#      await ctx.send(f"Your custom code is: {arg}")
#    elif role not in self.roles:
#      await ctx.send(f"You cannot use this command")
#    else:
#        await ctx.send(f"That is an incorrectly formatted code")

numb = 0


def increment():
  global numb
  numb = numb + 1


# Verification function
@bot.listen()
async def on_message(message):
  if message.author == client.user:
    return
    
  verify = []
    
  # listen for a student number
  if re.search("^[Nn][0-9]{6,12}",message.content):
    for i in range(4):
      # generate random unique verification code
      verify.append(str(random.randint(0, 9)))
      
    verify_code = ''.join(verify)

    global numb
    j = numb

    # Code to email the verification code
    sender = 'discordbotforin01@gmail.com'
    receiver = message.content + '@qut.edu.au'
    #receiver = 'discordbotforin01@gmail.com'
    body_send = "your verification code is: " + verify_code

    msg = MIMEText(body_send, 'html')
    msg['Subject'] = 'Verification'
    msg['From'] = sender
    msg['To'] = receiver
    s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    s.login(user = sender, password = os.getenv('GMAILPASS'))
    s.sendmail(sender, receiver, msg.as_string())
    s.quit()
    
    codes.append(f"{verify_code}")
    print(codes)
    increment()
    
    response = "Verification code sent to your QUT student email"
    await message.channel.send(response)
    print(f'{verify} is the code')
  elif message.content == 'raise-exception':
    raise discord.DiscordException

  # Listens for the verification code
  if re.search("[0-9]{4}",message.content):
    print("recieved")
    if message.content in codes:
      member = message.author
      removal = codes.index(message.content)
      print(removal)
      codes.pop(removal)
      # Change roles
      old_role = discord.utils.get(member.guild.roles, name="Visitor")
      temp_role = discord.utils.get(member.guild.roles, name="Visitor Temp")
      await member.remove_roles(old_role)
      await member.remove_roles(temp_role)
      role = discord.utils.get(member.guild.roles, name="Verified")
      await member.add_roles(role)
      await message.channel.send(f'User Verified')
      await member.create_dm()
      await member.dm_channel.send(
        f'Hi there! Thank you for verifying your account, welcome to the server :)'
      )
      

# Loop to change the status
@tasks.loop(seconds = 1440)
async def status_loop():
  status = ["qut!help for commands", "Check HiQ for info about QUT", "Don't forget to submit!", "Who doesn't love coding", "Why doesn't my Pi work?", "Programming is hard :(", "Can I join someone's group?", "Pokemon is cool!", f"Hi there! {version}"]
  for i in range(len(status)):
    await sleep(180)
    await bot.change_presence(activity=discord.Game(status[i]))


# Runs when the bot turns on
@bot.event
async def on_ready():
  global version
  global changelog
  guild = bot.get_guild(943354154129190922) # QUT server
  #guild = bot.get_guild(953551552562475048) # test server
  print("I'm in")
  
  # Sends changelog in announcements
  announcements = find(lambda x: x.name == 'announcements',  guild.text_channels)
  messages = await announcements.history(limit=4).flatten()
  if announcements and announcements.permissions_for(guild.me).send_messages:
    embed=discord.Embed(title=f"{version} Changelog", url="https://realdrewdata.medium.com/", description=f"{changelog}", color=discord.Color.dark_blue())
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
    embed.set_author(name="Emmey", icon_url="https://cdn.discordapp.com/attachments/835791348291469342/954362018884886528/IMG_20220303_125955_403.jpg")
    await announcements.send(embed=embed)
    
  # Begins the status changing
  await bot.change_presence(activity=discord.Game(f"Hi there! {version}"))
  status_loop.start()

# Runs when the bot joins a server
@bot.event
async def on_guild_join(guild):
  general = find(lambda x: x.name == 'general-general',  guild.text_channels)
  if general and general.permissions_for(guild.me).send_messages:
    await general.send("Hi there! I'm QUTBot, I don't have many features right now, but I hope you'll help me grow :D")

# assigns a new member the visitor role then DMs them
@bot.event 
async def on_member_join(member):
  role = get(member.guild.roles, name="Visitor")
  await member.add_roles(role)
  await member.create_dm()
  await member.dm_channel.send(
    f'{member.mention} Please send your QUT student number in #visitor (E.g: "n12345678"), then send the verification code that will be emailed to you.\n\n**Do Not Respond To This Message**'
  )

# Runs everything
def run():
  bot.add_cog(Moderation(bot))
  #bot.add_cog(Verification(bot))
  bot.add_cog(Info(bot))
  #bot.add_cog(Update(bot))
  bot.add_cog(Verify(bot))
  #bot.add_cog(Hiq(bot))
  #bot.add_cog(Issues(bot))
  bot.run(token)
  client.run(token)


if __name__ == "__main__":
  run()