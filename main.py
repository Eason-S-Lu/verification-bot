import discord
import random
import string
from dotenv import load_dotenv
import os

load_dotenv()

client = discord.Client()

verification_codes = {}

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!verify'):
        # ask for email address
        await message.channel.send('Please enter your email address:')
        email = await client.wait_for('message', check=lambda m: m.author == message.author)

        # generate and send verification code
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        await message.channel.send(f'Your verification code is: {code}. Please enter this code to verify your email address.')

        # store verification code and email
        verification_codes[message.author.id] = {'email': email.content, 'code': code}

    elif message.content.startswith('!code'):
        # check if user has a verification code stored
        if message.author.id not in verification_codes:
            await message.channel.send('You do not have a verification code.')
            return

        # check if verification code is correct
        if message.content[5:].strip() != verification_codes[message.author.id]['code']:
            await message.channel.send('Incorrect verification code.')
            return

        # give user the verified role
        role = discord.utils.get(message.guild.roles, name='verified')
        await message.author.add_roles(role)

        # remove verification code from storage
        del verification_codes[message.author.id]

        await message.channel.send('You have been verified!')
