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

from replit import db
from discord.utils import get

SKIP_BOTS = False

nav = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")

ending_note = "{ctx.bot.user.name} is not affiliated with QUT"

bot = commands.Bot(command_prefix="qut!", description="A bot to help with QUT servers")
client = discord.Client

bot.help_command = PrettyHelp(menu=nav, color=discord.Colour.blue(), ending_note=ending_note)

token = os.environ.get("DISCORD_TOKEN")


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

j = 0

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    
    verify = []
    
    j = 0
    
    if re.search("^n[0-9]{8}",message.content):
        for i in range(4):
            verify.append(str(random.randint(0, 9)))
        
        verify_code = ''.join(verify)
        
        
        sender = 'discordbotforin01@gmail.com'
        receiver = message.content + '@qut.edu.au'
        body_send = "your verification code is: " + verify_code

        msg = MIMEText(body_send, 'html')
        msg['Subject'] = 'Verification'
        msg['From'] = sender
        msg['To'] = receiver
        s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
        s.login(user = sender, password = os.getenv('GMAILPASS'))
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        
        db[f"code{j}"] = f"{verify_code}"
        db[f"user{j}"] = f"{message.content}"
        db[f"entry{j}"] = f"{j}"
        j = j + 1
        
        response = "Verification code sent"
        await message.channel.send(response)
        print(f'{verify} is the code')
    elif message.content == 'raise-exception':
        raise discord.DiscordException

    if re.search("[0-9]{4}",message.content):
      print("recieved")
      if message.content == db[f"code{j}"]:
        member = message.author
        await member.create_dm()
        await member.dm_channel.send(
          f'Hi there! Thank you for verifying your account, welcome to the server :)'
        )
        del db[f"code{j}"]
        del db[f"user{j}"]
        del db[f"entry{j}"]
        old_role = discord.utils.get(member.guild.roles, name="Visitor")
        await member.remove_roles(old_role)
        role = discord.utils.get(member.guild.roles, name="Verified")
        await member.add_roles(role)

@bot.event
async def on_ready():
  print("I'm in")

@client.event
async def on_error(event, *args, **kwargs):
    with open('logs/err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
  
def run():
  bot.add_cog(Moderation(bot))
  bot.run(token)

if __name__ == "__main__":
  run()