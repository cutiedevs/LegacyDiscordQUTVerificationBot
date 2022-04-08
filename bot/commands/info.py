import discord
from discord.ext import commands

from pretty_help import DefaultMenu, PrettyHelp

from asyncio import sleep

from os import getenv
from dotenv import load_dotenv

import python_weather

load_dotenv()

# Discord API token
token = getenv("DISCORD_TOKEN")

github_url = "https://github.com/Mistyttm/DiscordQUTVerificationBot"

class Info(commands.Cog):
    """Information commands"""
    @commands.command(
        name="info",
        brief="Info about the bot",
        help="Command to provide information about the bot"
    )
    async def _info(self, ctx):
        global version
        embed = discord.Embed(
            title=f"{version}",
            url=f"{github_url}",
            description=f"This bot was designed and developed by *Emmey Leo* for the QUT IN01 Discord server. It provides a system to verify that new members are QUT students. This project is completely open source and any and all people are allowed to contribute to the github:\n\n**https://github.com/Mistyttm/DiscordQUTVerificationBot**",
            color=discord.Color.dark_blue())
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
        await ctx.send(embed=embed)

    @commands.command(
        name="changelog",
        brief="Shows the changelog",
        help="Command to show all the changes in the current version of QUTBot"
    )
    async def _changelog(self, ctx):
        global version
        global changelog
        embed = discord.Embed(
            title=f"{version} Changelog",
            url=f"{github_url}",
            description=f"{changelog}",
            color=discord.Color.dark_blue())
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
        embed.set_author(
            name="Emmey",
            icon_url="https://cdn.discordapp.com/attachments/835791348291469342/954362018884886528/IMG_20220303_125955_403.jpg")
        await ctx.send(embed=embed)

    @commands.command(
        name="bug",
        brief="Gives new issue submission link",
        help="Command to provide the issues link for the QUTBot GitHub"
    )
    async def _bug(self, ctx):
        embed = discord.Embed(
            title=f"{version} Issue report",
            url=f"{github_url}",
            description=f"Please use this link to create a bug report:\n\nhttps://github.com/Mistyttm/DiscordQUTVerificationBot/issues/new/choose",
            color=discord.Color.red())
        await ctx.send(embed=embed)

    @commands.command(
        name="hiq",
        brief="Sends link to HiQ",
        help="Command to send the link directly to the HiQ homepage"
    )
    async def _hiq(self, ctx):
        embed = discord.Embed(
            title=f"{version} HiQ",
            url=f"{github_url}",
            description=f"HiQ:\n\nhttps://qutvirtual4.qut.edu.au/group/student/home",
            color=discord.Color.dark_blue())
        embed.set_thumbnail(
            url="https://qutvirtual4.qut.edu.au/image/image_gallery?uuid=acca9ca6-6d8c-4643-9351-d2f2c2b450eb&groupId=13901&filename=HiQlogo.jpg&t=1581892242556")
        await ctx.send(embed=embed)

    @commands.command(
        name="tones",
        brief="Tone Tags resource",
        help="Command to get help for understanding tone tags"
    )
    async def _hiq(self, ctx):
        embed = discord.Embed(
            title=f"{version} Tone Tags",
            url=f"{github_url}",
            description=f"A useful guide for tone tags:\n\nhttps://toneindicators.carrd.co/",
            color=discord.Color.dark_blue())
        await ctx.send(embed=embed)
    
    @commands.command(
        name="weather",
        brief="Tells you the weather at QUT",
        help="A command to tell you the current weather at QUT"
    )
    async def _weather(self, ctx):
        client = python_weather.Client()
        weather = await client.find("Brisbane")
        embed = discord.Embed(
            title=f"{version} Weather",
            url=f"{github_url}",
            description=f"The weather currently is: {weather.current.sky_text}\nThe current temperature is: {weather.current.temperature}°C",
            color=discord.Color.dark_blue())
        await ctx.send(embed=embed)
        await client.close()