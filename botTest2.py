# Libraries
import os
import asyncio
import discord
from dotenv import load_dotenv
from random import *
import re
import smtplib, ssl 
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart

#asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot is imported
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# command prefix
bot = commands.Bot(command_prefix='qut!')
client = discord.Client()

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test', help='Responds with a random number')
async def test(ctx):
    response = randint(1, 100)
    await ctx.send(response)

@bot.event
async def on_message(message):
    if message.author == client.user:
        return
    
    verify = []
    
    if re.search("^n[0-9]{8}",message.content):
        for i in range(4):
            verify.append(str(randint(0, 9)))
        
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
        
        
        response = "Verification code sent"
        await message.channel.send(response)
        print(f'{verify} is the code')
    elif message.content == 'raise-exception':
        raise discord.DiscordException


@client.event
async def on_error(event, *args, **kwargs):
    with open('logs/err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise
bot.run(TOKEN)
