# Libraries
import os
import asyncio
import discord
from dotenv import load_dotenv
import random
import re

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# bot is imported
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# command prefix
bot = commands.Bot(command_prefix='qut!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command(name='test', help='Responds with a random number')
async def test(ctx):
    response = randint(1,100)
    await ctx.send(response)


bot.run(TOKEN)
