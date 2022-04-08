import discord
from discord.ext import commands

from pretty_help import DefaultMenu, PrettyHelp

from asyncio import sleep

from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Discord API token
token = getenv("DISCORD_TOKEN")

class Moderation(commands.Cog):
    """All Moderation Commands"""

    def __init__(self, discord_token: str) -> None:
        self.base_api_url = 'https://discord.com/api/v8'
        self.auth_headers = {
            'Authorization': f'Bot {token}',
            'User-Agent': 'DiscordBot (https://discord.com/api/oauth2/authorize?client_id=953211624066539541&permissions=8&scope=bot) Python/3.10 aiohttp/3.8.1',
            'Content-Type': 'application/json'
        }

    @commands.command(
        name="mute",
        brief="Mute a member",
        help="Command to mute an unruly server member"
    )
    @commands.has_permissions(manage_messages=True)
    async def _mute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(
            member.guild.roles, name="Muted")

        await member.add_roles(muted_role)
        await member.send(f"You have been muted from: - {ctx.guild.name}")
        embed = discord.Embed(
            title=f"{version} Mute",
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
            description=f"Muted-{member.mention}",
            colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(
        name="unmute",
        brief="Un-mute a member",
        help="Command to Un-mute a server member"
    )
    @commands.has_permissions(manage_messages=True)
    async def _unmute(self, ctx, member: discord.Member):
        mutedRole = discord.utils.get(member.guild.roles, name="Muted")

        await member.remove_roles(mutedRole)
        await member.send(f"you have been un-muted from: - {ctx.guild.name}")
        embed = discord.Embed(
            title=f"{version} Unmute",
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
            description=f"Un-muted-{member.mention}",
            colour=discord.Colour.dark_blue())
        await ctx.send(embed=embed)

    @commands.command(
        name="clear",
        brief="Clear chat",
        help="Command for moderators to automatically clear chat"
    )
    @commands.has_role('Moderator')
    async def _clear(self, ctx, amount: int):
        await ctx.channel.purge(limit=amount)

    @commands.command(
        name="ban",
        brief="Ban a member",
        help="Command to ban a member from the discord"
    )
    @commands.has_permissions(ban_members=True)
    async def _ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)

    @commands.command(
        name="unban",
        brief="Un-ban a user",
        help="Command to un-ban a user"
    )
    @commands.has_permissions(administrator=True)
    async def _unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command(
        pass_context=True,
        name="kick",
        brief="Kick a member",
        help="Command to kick a member from the server"
    )
    @commands.has_permissions(kick_members=True)
    async def _kick(self, ctx, userName: discord.User):
        await bot.kick(userName)