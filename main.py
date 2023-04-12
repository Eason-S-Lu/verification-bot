import discord
from discord.ext import commands
import smtplib
import random
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ALLOWED_DOMAINS = ['pausd.us', 'example.org'] # replace with the domains you want to allow

intents = discord.Intents.default()
intents.members = True

def generate_verification_code():
    return str(random.randint(100000, 999999))

def send_verification_email(recipient_email, verification_code):
    if recipient_email.split('@')[-1] not in ALLOWED_DOMAINS:
        return

    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    message = f'Subject: Verification Code\n\nYour verification code is {verification_code}'

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, recipient_email, message)

async def send_verification_code(ctx):
    verification_code = generate_verification_code()
    send_verification_email(ctx.author.email, verification_code)

    await ctx.send(f'Please enter the verification code sent to your email, {ctx.author.mention}.')

    def check_verification_code(message):
        return message.author == ctx.author and message.content == verification_code

    try:
        message = await client.wait_for('message', timeout=60.0, check=check_verification_code)
    except asyncio.TimeoutError:
        await ctx.send('Verification timed out. Please try again.')
    else:
        role = discord.utils.get(ctx.guild.roles, name='Verified')
        await ctx.author.add_roles(role)
        await ctx.send('You have been verified!')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_member_join(member):
    await member.send(f'Welcome to the server, {member.mention}! Please verify yourself by using the `!verify` command.')

@bot.command()
async def verify(ctx):
    await send_verification_code(ctx)

bot.run(BOT_TOKEN)
