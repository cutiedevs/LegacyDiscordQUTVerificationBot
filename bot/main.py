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
from random import *

from smtplib import SMTP_SSL
from email.utils import formataddr
from email.mime.text import MIMEText

import commands.moderation as mod
import commands.verification as verify
import commands.info as info

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
version = "QUTBot v1.5.2"
changelog = "- Changed some things in the backend\n\nCheckout the code on Github: **https://github.com/Mistyttm/DiscordQUTVerificationBot**"


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have all the requirements :angry:")

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
        "Prioritize being hot", "Lambageddon"]

    status_rand = randrange(len(status))
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
            url="https://github.com/Mistyttm/DiscordQUTVerificationBot",
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
    bot.add_cog(mod.Moderation(bot))
    bot.add_cog(info.Info(bot))
    bot.add_cog(verify.Verification(bot))
    # bot.add_cog(Study(bot))

    bot.run(token)


if __name__ == "__main__":
    run()
