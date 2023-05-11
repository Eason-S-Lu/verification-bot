import discord
from discord.ext import commands
import smtplib
import random
import os
import logging
from dotenv import load_dotenv
import asyncio

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
SMTP_USERNAME = os.getenv('SMTP_USERNAME')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
ALLOWED_DOMAINS = ['pausd.us']  # replace with the domains you want to allow

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="~", intents=intents)

logging.basicConfig(level=logging.DEBUG)


def generate_verification_code():
  return str(random.randint(100000, 999999))


async def send_verification_email(email, verification_code):
  if email.split('@')[-1] not in ALLOWED_DOMAINS:
    return f'Error: {email} is not a valid email address for verification. Please use @pausd.us instead, or contact an admin.'

  smtp_server = 'smtp.gmail.com'
  smtp_port = 587

  message = f'Subject: Verification Code\n\nYour verification code is {verification_code}'

  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    server.login(SMTP_USERNAME, SMTP_PASSWORD)
    server.sendmail(SMTP_USERNAME, email, message)

  logging.debug(f'Verification code {verification_code} sent to {email}.')


async def send_verification_code(ctx):
  await ctx.send(
    'Please enter your email address to receive a verification code.')

  def check_email(message):
    return message.author == ctx.author and '@' in message.content and isinstance(
      message.channel, discord.TextChannel)

  try:
    message = await bot.wait_for('message', timeout=30.0, check=check_email)
  except asyncio.TimeoutError:
    await ctx.send('Verification timed out. Please try again.')
    return

  email = message.content.strip()

  if email.split('@')[-1] not in ALLOWED_DOMAINS:
    await ctx.send(
      f'Error: {email} is not a valid email address for verification. Please use @pausd.us instead, or contact an admin.'
    )
    return

  verification_code = generate_verification_code()
  send_result = await send_verification_email(email, verification_code)

  if send_result is not None:
    await ctx.send(send_result)
    return

  await ctx.send(f'Please enter the verification code sent to {email}.')

  def check_verification_code(message):
    return message.author == ctx.author and message.content == verification_code and isinstance(
      message.channel, discord.TextChannel)

  try:
    message = await bot.wait_for('message',
                                 timeout=30.0,
                                 check=check_verification_code)
  except asyncio.TimeoutError:
    await ctx.send('Verification timed out. Please try again.')
    return

  guild = ctx.guild
  member = guild.get_member(ctx.author.id)
  role = discord.utils.get(guild.roles, name='Verified')
  await member.add_roles(role)
  role = discord.utils.get(guild.roles, name='Member')
  await member.add_roles(role)
  await ctx.send('You have been verified!')


@bot.event
async def on_ready():
  logging.info('Bot is ready.')


@bot.event
async def on_member_join(member):
  user = member
  await user.send(
    f'Welcome to the server, {user.mention}! Please verify yourself by using the `~verify` command.'
  )


@bot.command()
async def verify(ctx):
  await send_verification_code(ctx)


bot.run(BOT_TOKEN)
