### Libraries ###
import discord
from discord.ext import commands
from discord.utils import get
from discord.utils import find
from discord.ext import tasks

from pretty_help import DefaultMenu, PrettyHelp

from asyncio import sleep

from os import getenv
from dotenv import load_dotenv

from re import findall
from random import randint

from smtplib import SMTP_SSL
from email.utils import formataddr
from email.mime.text import MIMEText

# import ifb102_quiz_1 as q
### End Libraries ###

# Load environment variables
load_dotenv()

# Discord API token
token = getenv("DISCORD_TOKEN")

# Bot
intents = discord.Intents.all()
bot = commands.Bot(
    command_prefix="qut!",
    description="A bot to help with QUT servers", intents=intents)

# Client
client = discord.Client
# Client = Bot('qut!')

# Guild
guild = bot.get_guild(int(getenv("GUILD_ID")))

# Embed customisation
nav = DefaultMenu(page_left="◀️", page_right="▶️", remove="❌")
ending_note = f"QUTBot is not affiliated with QUT"
bot.help_command = PrettyHelp(
    menu=nav, color=discord.Colour.blue(), ending_note=ending_note)

# Verification codes
codes = []

# Changelog
version = "QUTBot v1.5.0"
changelog = "\n- Verification system has been overhauled\n\nThank you to **LightninBolt74** for helping with this update :)\n\nCheckout the code on Github: **https://github.com/Mistyttm/DiscordQUTVerificationBot**"


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have all the requirements :angry:")


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
    async def _kick(self, ctx, userName: discord.User):
        await bot.kick(userName)


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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
            description=f"A useful guide for tone tags:\n\nhttps://toneindicators.carrd.co/",
            color=discord.Color.dark_blue())
        await ctx.send(embed=embed)

# Verification function
@bot.listen()
async def on_message(message: discord.Message):
    # Ignore bot messages
    if message.author.bot:
        return

    # Message must be sent in verification channel    
    verification_channel = bot.get_channel(int(getenv("VERIFICATION_CHANNEL_ID")))
    if message.channel.id != verification_channel.id:
        return

    # Listen for a student number
    student_number = findall(r"([Nn]?[0-9]{6,12})", message.content)
    if student_number:
        # Generate random unique verification code
        verification_code = f"{randint(0, 9999):04}"

        # Code to email the verification code
        sender = 'discordbotforin01@gmail.com'
        
        # Check if 'n' was given in message
        if student_number[0][0].lower() != 'n':
            receiver = f"n{student_number[0]}@qut.edu.au"
        else:
            receiver = f"{student_number[0]}@qut.edu.au"
        # receiver = 'discordbotforin01@gmail.com'

        body_send = f'''<html><head><link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">
<style>
    .main_container {{
        padding: 0 10rem;
        font-family: 'Open Sans', sans-serif;
    }}

    .heading_text {{
        margin: 0.8rem 0;
        font-weight: 600;
        font-size: 3.5rem;
    }}

    .main_text {{
        margin: 1em 0;
        font-weight: 400;
        font-size: 1.5rem;
    }}

    .verification_code {{
        padding: 0 32px;
        font-family: JetBrains Mono, sans-serif;
        font-size: 112px;
        line-height: 1;
        color: #020202;
        font-weight: bold;
        letter-spacing: 5px;
        text-align: center;
    }}

    .footer_text {{
        margin: 3em 0;
        font-weight: 400;
        font-size: 1rem;
    }}

</style>
</head>
<body>
<div class="main_container">
    <div class="heading_text">
        Your verification code for {message.guild.name}
    </div>
    <div class="main_text">
        Hi <strong style="font-weight:600;">{message.author}</strong>,<br>
        Your verification code is:
    </div>
    <div class="verification_code">
        {verification_code}
    </div>
    <div class="footer_text" style="text-align: center;">
        Thank you for using our bot.
    </div>
    <hr>
    <div class="footer_text">
        You are receiving this message because this student number was
        used to verify a Discord account. If you did not request this 
        code please disregard this message.
    </div>
</div>
</body>
</html>'''

        # Setup email
        msg = MIMEText(body_send, 'html')
        msg['Subject'] = 'Discord Verification Code'
        msg['From'] = formataddr(('QUTBot', sender))
        msg['To'] = receiver
        
        s = SMTP_SSL(host='smtp.gmail.com', port=465)
        s.login(user=sender, password=getenv('GMAILPASS'))
        s.sendmail(sender, receiver, msg.as_string())
        s.quit()
        
        # Delete message from user
        await message.delete()

        codes.append([verification_code, message.author])

        print("Active verification codes:")
        print(codes)

        response = f"{message.author.mention} A verification code has been sent to your QUT student email"
        await message.channel.send(response)

    # Check if codes are ready to be verified
    if not codes:
        return

    # Listens for the verification code
    verification_code = findall(r"([0-9]{4})", message.content)
    if verification_code:
        # Ensure that the user provides the correct code
        if [verification_code[0], message.author] in codes:
            print(f"Received verification code from {message.author}")
            codes.pop(codes.index([verification_code[0], message.author]))

            member = message.author
            
            # Remove visitor role
            old_role = discord.utils.get(
                member.guild.roles, name="Visitor")
            temp_role = discord.utils.get(
                member.guild.roles, name="Visitor Temp")

            await member.remove_roles(old_role)
            await member.remove_roles(temp_role)

            # Add verified role
            role = discord.utils.get(
                member.guild.roles, name="Verified")
            await member.add_roles(role)

            # Delete message from user
            await message.delete()

            await member.create_dm()
            try:
                await member.dm_channel.send(
                    f'Hi there! Thank you for verifying your account, welcome to the server :)'
                )
            except discord.errors.Forbidden:
                print(f"{message.author} has disabled dms from server members")

# Loop to change the status
@tasks.loop(seconds=180)
async def status_loop():
    status = [
        "qut!help for commands", "Check HiQ for info about QUT",
        "Don't forget to submit!", "Who doesn't love coding",
        "Why doesn't my Pi work?", "Programming is hard :(",
        "Can I join someone's group?", "Pokemon is cool!",
        f"Hi there! {version}",
        "Why are these guys so hard on collusion?", "t u r t l e",
        "Don't use Chegg", "APA or Harvard", "qut!help gets you help",
        "That's not very slay yass of u", "In my reputation era",
        "Getting them girlboss vibes",
        "Feeling submissive and breedable", "Trans rights",
        "No sleep, only program", "Fish fear me",
        "Dreading my existence", "What is my purpose?",
        "Prioritize being hot"]

    status_rand = randint(0, len(status))
    await sleep(180)
    await bot.change_presence(activity=discord.Game(status[status_rand]))


# Runs when the bot turns on
@bot.event
async def on_ready():
    global version
    global changelog
    guild = bot.get_guild(int(getenv("GUILD_ID")))
    print("I'm in")
    # print(changelog_sent)

    # Sends changelog in announcements
    announcements = find(lambda x: x.name ==
                         'announcements', guild.text_channels)
    if announcements and announcements.permissions_for(
            guild.me).send_messages:
        embed = discord.Embed(
            title=f"{version} Changelog",
            url="https://realdrewdata.medium.com/",
            description=f"{changelog}",
            color=discord.Color.dark_blue())
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/943355996934402119/954311293249138708/qut-bot-logo.png?width=663&height=663")
        embed.set_author(
            name="Emmey",
            icon_url="https://cdn.discordapp.com/attachments/835791348291469342/954362018884886528/IMG_20220303_125955_403.jpg")
        await announcements.send(embed=embed)

    # Begins the status changing
    await bot.change_presence(activity=discord.Game(f"Hi there! {version}"))
    status_loop.start()

# Runs when the bot joins a server

@bot.event
async def on_guild_join(guild: discord.Guild):
    general = find(lambda x: x.name ==
                   'general-general', guild.text_channels)
    if general and general.permissions_for(guild.me).send_messages:
        await general.send("Hi there! I'm QUTBot, I don't have many features right now, but I hope you'll help me grow :D")

# assigns a new member the visitor role then DMs them
@bot.event
async def on_member_join(member: discord.Member):
    role = get(member.guild.roles, name="Visitor")
    await member.add_roles(role)

    await member.create_dm()
    try:
        await member.dm_channel.send(
            f'{member.mention} Please send your QUT student number in #visitor (E.g. "n12345678"), then send the verification code that will be emailed to you.\n\n**Do Not Respond To This Message**'
        )
    except discord.errors.Forbidden:
        print(f"{member.name} has disabled dms from server members")


# Runs everything
def run():
    bot.add_cog(Moderation(bot))
    bot.add_cog(Info(bot))
    bot.add_cog(Verification(bot))
    # bot.add_cog(Study(bot))

    bot.run(token)
    client.run(token)


if __name__ == "__main__":
    run()
