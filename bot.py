# bot.py
import os
import asyncio
import discord
from dotenv import load_dotenv
import random
import re

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

#@client.event
#async def on_member_join(member):
#    await member.create_dm()
#    await member.dm_channel.send(
#        f'Hi {member.name}, welcome to the QUT Bachelor'
#    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if re.search("^n[0-9]{8}",message.content):
        response = "Verification code sent"
        await message.channel.send(response)
    elif message.content == 'raise-exception':
        raise discord.DiscordException

@client.event
async def on_error(event, *args, **kwargs):
    with open('logs/err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise


client.run(TOKEN)
