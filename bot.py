# bot.py
import os
import asyncio
import discord
from dotenv import load_dotenv

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has conected to discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, Welcome to my Discord server!'
    )

# class CustomClient(discord.Client):
#     async def on_ready(self):
#         print(f'{self.user} has conected to discord!')

# @client.event
# async def on_ready():
#     guild = discord.utils.get(client.guilds, name=GUILD)
#     print(
#         f'{client.user} is connected to the following guild:\n'
#         f'{guild.name}(id: {guild.id})'
#         )

# client = CustomClient()
client.run(TOKEN)
