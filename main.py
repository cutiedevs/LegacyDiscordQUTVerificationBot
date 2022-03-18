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

class Moderation(commands.Cog):
  """All Moderation Commands"""
  @commands.command(
    name="test",
    brief="test",
    help="test"
  )
  async def _test(self, ctx):
    num = random.randint(1,100)
    await ctx.send(f"{ctx.message.author.mention} your number is {num}")

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

class Info(commands.Cog):
  """Information commands"""
  @commands.command(
    name="info",
    brief="Info about the bot",
    help="Command to provide information about the bot"
  )
  async def _info(self, ctx):
    embed=discord.Embed(title="QUTBot v1.2.1", url="https://realdrewdata.medium.com/", description=f"This bot was designed and programmed by *Emmey Leo* for the QUT IN01 Discord. It provides a system to verify that new members are qut students. This project is completely open source and any and all people are allowed to contribute to the github:\n\n**https://github.com/Mistyttm/DiscordQUTVerificationBot**", color=discord.Color.dark_blue())
    await ctx.send(embed=embed)
  
  @commands.command(
    name="verify",
    brief="Instructions on how to verify",
    help="Command to provide information about how to verify your account"
  )
  async def _info(self, ctx):
    embed=discord.Embed(title="Verification Instructions", url="https://realdrewdata.medium.com/", description=f"1. Go to #verification\n2. Send your student number e.g. n12345678\n3. Check your QUT email for the verification code\n4. Send the verification code in #verification", color=discord.Color.dark_blue())
    await ctx.send(embed=embed)
  
  @commands.command(
    name="changelog",
    brief="Shows the changelog",
    help="Command to show all the changes in the current version of QUTBot"
  )
  async def _info(self, ctx):
    embed=discord.Embed(title="QUTBot v1.2.1 Changelog", url="https://realdrewdata.medium.com/", description=f"- Added support for student numbers between 6 and 12 characters\n- Added update announcements\n- Added a command to view the changelog\n\nCheckout the code on Github: **https://github.com/Mistyttm/DiscordQUTVerificationBot**", color=discord.Color.dark_blue())
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


@bot.listen()
async def on_message(message):
  if message.author == client.user:
    return
    
  verify = []
    
  if re.search("^n[0-9]{6,12}",message.content):
    for i in range(4):
      verify.append(str(random.randint(0, 9)))
      
    verify_code = ''.join(verify)

    global numb
    j = numb

    
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

  if re.search("[0-9]{4}",message.content):
    print("recieved")
    if message.content in codes:
      member = message.author
      removal = codes.index(message.content)
      print(removal)
      codes.pop(removal)
      old_role = discord.utils.get(member.guild.roles, name="Visitor")
      await member.remove_roles(old_role)
      role = discord.utils.get(member.guild.roles, name="Verified")
      await member.add_roles(role)
      await member.create_dm()
      await member.dm_channel.send(
        f'Hi there! Thank you for verifying your account, welcome to the server :)'
      )
      

@bot.event
async def on_ready():
  guild = bot.get_guild(943354154129190922)
  print("I'm in")
  announcements = find(lambda x: x.name == 'announcements',  guild.text_channels)
  if announcements and announcements.permissions_for(guild.me).send_messages:
    embed=discord.Embed(title="QUTBot v1.2.0 Changelog", url="https://realdrewdata.medium.com/", description=f"- Added support for student numbers between 6 and 12 characters\n- Added update announcements\n\nCheckout the code on Github: **https://github.com/Mistyttm/DiscordQUTVerificationBot**", color=discord.Color.dark_blue())
    await announcements.send(embed=embed)

@bot.event
async def on_guild_join(guild):
  general = find(lambda x: x.name == 'general-general',  guild.text_channels)
  if general and general.permissions_for(guild.me).send_messages:
    await general.send("Hi there! I'm QUTBot, I don't have many features right now, but I hope you'll help me grow :D")

@bot.event 
async def on_member_join(member):
  role = get(member.guild.roles, name="Visitor")
  await member.add_roles(role)
  await member.create_dm()
  await member.dm_channel.send(
    f'{member.mention} Please send your QUT student number in #visitor (E.g: "n12345678"), then send the verification code that will be emailed to you.\n\n**Do Not Respond To This Message**'
  )
  
def run():
  bot.add_cog(Moderation(bot))
  #bot.add_cog(Verification(bot))
  bot.add_cog(Info(bot))
  bot.run(token)
  client.run(token)

if __name__ == "__main__":
  run()