# Libraries
import os
import asyncio
import discord
from dotenv import load_dotenv
from random import *
import re

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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
            verify.append(randint(0, 9))
        response = "Verification code sent"
        await message.channel.send(response)
        print(f'{verify} is the code')
    elif message.content == 'raise-exception':
        raise discord.DiscordException


bot.run(TOKEN)
