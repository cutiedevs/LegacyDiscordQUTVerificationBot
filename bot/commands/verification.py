import discord
from discord.ext import commands

from pretty_help import DefaultMenu, PrettyHelp

from asyncio import sleep

from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Discord API token
token = getenv("DISCORD_TOKEN")

class Verification(commands.Cog):
    """All Verification Commands"""
    @commands.command(
        name="verify",
        brief="Instructions on how to verify",
        help="Command to provide information about how to verify your account"
    )
    async def _info(self, ctx):
        embed = discord.Embed(
            title="Verification Instructions",
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
            description=f"1. Go to #verification\n2. Send your student number e.g. `n12345678`\n3. Check your QUT email for the verification code\n4. Send the verification code in #verification",
            color=discord.Color.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(
        name="clearcodes",
        brief="Clears verification codes",
        help="This command removes all stored verification codes, users who have not used their code will need another one"
    )
    @commands.has_role('Moderator')
    async def _removeCodes(self, ctx):
        global codes
        codes.clear()
        print(codes)
        await ctx.send("All verification codes have been deleted")

    @commands.command(
        name="addcode",
        brief="Adds a custom code",
        help="This command adds a custom 4 number code for moderators to give out"
    )
    @commands.has_role('Moderator')
    async def _addCodes(self, ctx, arg,):
        global codes
        codes.append(arg)
        print(codes)
        await ctx.send(f"Your custom code is: {arg}")